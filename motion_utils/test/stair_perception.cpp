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
#include "motion_utils/stair_perception.hpp"

namespace cyberdog
{
namespace motion
{

StairPerception::StairPerception(rclcpp::Node::SharedPtr node, const toml::value& config)
{
  node_ = node;
  // RCLCPP_INFO(node_->get_logger(), "This is an info message");  
  INFO("------www----------");
  pc_raw_.reset(new pcl::PointCloud<pcl::PointXYZ>);

  GET_TOML_VALUE(config, "radius", radius_);
  GET_TOML_VALUE(config, "min_neighbors", min_neighbors_);
  GET_TOML_VALUE(config, "orientation_dead_zone", orientation_dead_zone_);
  GET_TOML_VALUE(config, "orientation_correction", orientation_correction_);
  GET_TOML_VALUE(config, "orientation_filter", orientation_filter_);
  GET_TOML_VALUE(config, "filter_size", filter_size_);
  GET_TOML_VALUE(config, "blind_forward_threshold", blind_forward_threshold_);
  toml::value thresholds;
  GET_TOML_VALUE(config, "approach_threshold", thresholds);
  for(size_t i = 0; i < thresholds.size(); ++i) {
    toml::value threshold = thresholds.at(i);
    std::array<float, 2> z_range;
    int approach_threshold;
    GET_TOML_VALUE(threshold, "z_range", z_range);
    GET_TOML_VALUE(threshold, "threshold", approach_threshold);
    approach_thresholds_.emplace_back(ApproachThreshold{z_range, approach_threshold});
  }
  pc_filtered_.reset(new pcl::PointCloud<pcl::PointXYZ>);
  ro_filter_.setRadiusSearch(radius_);
  ro_filter_.setMinNeighborsInRadius(min_neighbors_);

  pcl_sub_ = node_->create_subscription<sensor_msgs::msg::PointCloud2>("/mi_desktop_48_b0_2d_7b_02_9c/head_pc",
  rclcpp::SystemDefaultsQoS(),
  std::bind(&StairPerception::HandlePointCloud, this, std::placeholders::_1));

  pc_ro_filtered_pub_ = node_->create_publisher<sensor_msgs::msg::PointCloud2>("ro_filtered22", 1);

  state_ = State::IDLE;
  trigger_ = true;
}

void StairPerception::HandlePointCloud(const sensor_msgs::msg::PointCloud2 & msg)
{
  // INFO("----------1------");
  // if(!launch_) {
  //   return;
  // }
  // INFO("-----------2-----");
  pcl::fromROSMsg(msg, *pc_raw_);
  ro_filter_.setInputCloud(pc_raw_);
  ro_filter_.filter(*pc_filtered_);
  pcl::toROSMsg(*pc_filtered_, pc_filtered_ros_);
  pc_ro_filtered_pub_->publish(pc_filtered_ros_);
  int total_points_size = pc_filtered_->size();
  int left_point_size = 0;
  int right_point_size = 0;
  // int dead_zone = 2, correction = 0;


  float z = 0, sum = 0;
  for (auto point : pc_filtered_->points) {
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
  }
  z = sum / pc_filtered_->points.size();
  for (auto threshold : approach_thresholds_) {
    if( z > threshold.range.front() && z <= threshold.range.back()) {
      approach_threshold_ = threshold.threshold;
      break;
    }
  }
  INFO("left: %d, right: %d, z: %f, th: %d", left_point_size, right_point_size, z, approach_threshold_);
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
      if (total_points_size < blind_forward_threshold_) {
        INFO("Points size %d < threshold, stair not found, Blind Forward", total_points_size);
        break;
      }
      if (diff < -orientation_dead_zone_ + orientation_correction_) {
        INFO("Turn right: %d", diff);
        state_ = State::TURN_RIGHT;
      } else if (diff > orientation_dead_zone_ + orientation_correction_) {
        INFO("Turn left: %d", diff);
        state_ = State::TURN_LEFT;
      } else {
        INFO("Approach Directly: %d", diff);
        state_ = State::APPROACH;
      }
      break;

    case State::TURN_LEFT:
      if (diff <= orientation_dead_zone_ + orientation_correction_) {
        if (total_points_size > approach_threshold_) {
          INFO("Finish turning left: %d", diff);
          state_ = State::FINISH;
        } else {
          INFO("Will approach when turning left: %d", total_points_size);
          state_ = State::APPROACH;
        }
      }
      INFO("Turn left: %d", diff);
      break;

    case State::TURN_RIGHT:
      if (diff >= -orientation_dead_zone_ + orientation_correction_) {
        if(total_points_size > approach_threshold_) {
          INFO("Finish turning right: %d", diff);
          state_ = State::FINISH;
        } else {
          INFO("Will approach when turning right: %d", total_points_size);
          state_ = State::APPROACH;
        }
      }
      INFO("Turn right: %d", diff);
      break;

    case State::APPROACH:
      if (total_points_size > approach_threshold_) {
        INFO("Stop: %d", total_points_size);
        state_ = State::FINISH;
      }
      INFO("Approaching: %d", total_points_size);
      break;

    case State::FINISH:
      WARN("------------FINISH");
      state_ = State::IDLE;
      trigger_ = true;
      break;

    default:
      break;
  }
}
}
}
