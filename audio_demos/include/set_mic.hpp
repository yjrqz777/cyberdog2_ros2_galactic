// Copyright (c) 2023-2023 Beijing Xiaomi Mobile Software Co., Ltd. All rights reserved.
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
#ifndef SET_MIC_HPP_
#define SET_MIC_HPP_

#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "protocol/srv/audio_execute.hpp"
#include "protocol/msg/audio_status.hpp"
class AudioSetMic : public rclcpp::Node
{
public:
  AudioSetMic()
  : Node("AudioSetMic")
  {
    name_ = "AudioSetMic";
    group_ = this->create_callback_group(
      rclcpp::CallbackGroupType::Reentrant);
    audio_client_ =
      this->create_client<protocol::srv::AudioExecute>(
      "set_audio_state",
      rmw_qos_profile_services_default, group_);
    // 使用timer触发
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(1000), std::bind(&AudioSetMic::timer_callback, this));
  }

private:
  void timer_callback()
  {
    if (audio_client_ == nullptr) {
      RCLCPP_INFO(this->get_logger(), "audio client not ready.");
    } else {
      if (!audio_client_->wait_for_service(std::chrono::seconds(2))) {
        RCLCPP_INFO(this->get_logger(), "call mic state server not avalible");
      } else {
        std::chrono::seconds timeout(3);
        auto req = std::make_shared<protocol::srv::AudioExecute::Request>();
        req->client = name_;
        // 打开、关闭mic
        req->status.state = protocol::msg::AudioStatus::AUDIO_STATUS_NORMAL;
        //  protocol::msg::AudioStatus::AUDIO_STATUS_OFFMIC;
        auto res = audio_client_->async_send_request(req);
        std::future_status status = res.wait_for(timeout);
        if (status != std::future_status::ready) {
          RCLCPP_INFO(this->get_logger(), "Failed to call audio execute services.");
          return;
        }
        RCLCPP_INFO(this->get_logger(), "Set mic done.");
        rclcpp::shutdown();
      }
    }
  }
  rclcpp::CallbackGroup::SharedPtr group_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Client<protocol::srv::AudioExecute>::SharedPtr audio_client_ = nullptr;

  std::string name_;
};

#endif  // SET_MIC_HPP_
