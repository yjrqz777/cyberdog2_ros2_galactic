// Copyright (c) 2023 Beijing Xiaomi Mobile Software Co., Ltd. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#include "motion_utils/edge_perception.hpp"

namespace cyberdog
{
namespace motion
{

EdgePerception::EdgePerception(rclcpp::Node::SharedPtr node, const toml::value& config)
{
  node_ = node;

  pc_raw_.reset(new pcl::PointCloud<pcl::PointXYZ>);
  GET_TOML_VALUE(config, "radius", radius_);
  GET_TOML_VALUE(config, "min_neighbors", min_neighbors_);
  GET_TOML_VALUE(config, "orientation_dead_zone", orientation_dead_zone_);
  GET_TOML_VALUE(config, "orientation_correction", orientation_correction_);
  GET_TOML_VALUE(config, "orientation_filter", orientation_filter_);
  GET_TOML_VALUE(config, "filter_size", filter_size_);
  GET_TOML_VALUE(config, "blind_forward_threshold", blind_forward_threshold_);
  GET_TOML_VALUE(config, "threshold", approach_threshold_);
  GET_TOML_VALUE(config, "max_depth", max_depth_);

  pc_rofiltered_.reset(new pcl::PointCloud<pcl::PointXYZ>);
  ro_filter_.setRadiusSearch(radius_);
  ro_filter_.setMinNeighborsInRadius(min_neighbors_);

  pc_ptfiltered_.reset(new pcl::PointCloud<pcl::PointXYZ>);
  pt_filter_.setFilterFieldName("z");
  pt_filter_.setFilterLimits(-0.35, -0.1);

  pcl_sub_ = node_->create_subscription<sensor_msgs::msg::PointCloud2>(
    "head_pc",
    rclcpp::SystemDefaultsQoS(),
    std::bind(&EdgePerception::HandlePointCloud, this, std::placeholders::_1));
  pc_ro_filtered_pub_ = node_->create_publisher<sensor_msgs::msg::PointCloud2>("ro_filtered", 1);
  state_ = State::IDLE;
  trigger_ = true;
  is_edge_deep_ = false;
}

void EdgePerception::HandlePointCloud(const sensor_msgs::msg::PointCloud2 & msg)
{
  if(!launch_) {
    return;
  }
  INFO("----------------");
  pcl::fromROSMsg(msg, *pc_raw_);
  ro_filter_.setInputCloud(pc_raw_);
  ro_filter_.filter(*pc_rofiltered_);
  pt_filter_.setInputCloud(pc_rofiltered_);
  pt_filter_.filter(*pc_ptfiltered_);

  pcl::toROSMsg(*pc_ptfiltered_, pc_filtered_ros_);
  pc_ro_filtered_pub_->publish(pc_filtered_ros_);
  int total_points_size = pc_ptfiltered_->size();
  int left_point_size = 0;
  int right_point_size = 0;
  // int dead_zone = 2, correction = 0;
  float z = 0, sum = 0;
  float x_filtered_max = 0;
  float z_beyond_xfmax = 0, sum_beyond_xfmax = 0;
  int beyond_xfmax_point_size = 0;
  for (auto point : pc_ptfiltered_->points) {
    if (point.y > 0) {
      left_point_size++;
    } else {
      right_point_size++;
    }
    // TODO(): 去除极大极小值
    // if(abs(point.z) <= 0.05 ) {
    //   continue;
    // }
    sum += abs(point.z);
    if (point.x > x_filtered_max)
        x_filtered_max = point.x;
  }
  z = total_points_size > 0 ? sum / total_points_size : 0.5;

  for (auto point : pc_raw_->points) {
    if (point.x > x_filtered_max) {
        beyond_xfmax_point_size++;
        sum_beyond_xfmax += abs(point.z);
    }
  }
  z_beyond_xfmax = beyond_xfmax_point_size > 0 ? sum_beyond_xfmax / beyond_xfmax_point_size : 0.5;
  is_edge_deep_ = (z_beyond_xfmax > max_depth_);
  INFO("left: %d, right: %d, total: %d, z: %f", left_point_size, right_point_size, total_points_size, z);
  INFO("z_beyond_xfmax: %f, beyond_xfmax_point_size: %d",z_beyond_xfmax, beyond_xfmax_point_size);
  int diff = 0;
  if (orientation_filter_) {
    diff = GetMeanDiff(left_point_size - right_point_size);
  } else {
    diff = left_point_size - right_point_size;
  }
  switch (state_) {
    case State::IDLE:
      if (trigger_) {
        state_ = State::BLIND_FORWARD;
        trigger_ = false;
        INFO("Launch!");
      }
      break;

    case State::BLIND_FORWARD:
      if (total_points_size > blind_forward_threshold_) {
        INFO("Points size %d < threshold, edge not found, Blind Forward", total_points_size);
        break;
      }
      if (diff > orientation_dead_zone_ + orientation_correction_) {
        INFO("Turn right: %d", diff);
        state_ = State::TURN_RIGHT;
      } else if (diff < -orientation_dead_zone_ + orientation_correction_) {
        INFO("Turn left: %d", diff);
        state_ = State::TURN_LEFT;
      } else if (total_points_size < approach_threshold_ + 20){
        INFO("Approach Directly: %d", diff);
        state_ = State::APPROACH;
      }
      break;

    case State::TURN_LEFT:
      if (diff >= -orientation_dead_zone_ + orientation_correction_) {
        if (total_points_size < approach_threshold_) {
          INFO("Finish turning left: %d", diff);
          state_ = State::FINISH;
        } else if (total_points_size < approach_threshold_ + 20){
          INFO("Will approach when turning left: %d", total_points_size);
          state_ = State::APPROACH;
        } else {
          state_ = State::BLIND_FORWARD;
        }
      }
      INFO("Turn left: %d", diff);
      break;

    case State::TURN_RIGHT:
      if (diff <= orientation_dead_zone_ + orientation_correction_) {
        if(total_points_size < approach_threshold_) {
          INFO("Finish turning right: %d", diff);
          state_ = State::FINISH;
        } else if (total_points_size < approach_threshold_ + 20){
          INFO("Will approach when turning right: %d", total_points_size);
          state_ = State::APPROACH;
        } else {
          state_ = State::BLIND_FORWARD;
        }
      }
      INFO("Turn right: %d", diff);
      break;

    case State::APPROACH:
      if (total_points_size < approach_threshold_) {
        INFO("Stop: %d", total_points_size);
        state_ = State::FINISH;
      }
      INFO("Approaching: %d", total_points_size);
      break; 

    case State::FINISH:
      break;

    default:
      break;
  }
}
}
}
