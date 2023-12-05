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
#ifndef SET_VOICE_HPP_
#define SET_VOICE_HPP_
#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"
#include "std_msgs/msg/u_int8.hpp"
class AudioSetVoiceDemo : public rclcpp::Node
{
public:
  AudioSetVoiceDemo()
  : Node("AudioSetVoiceDemo")
  {
    name_ = "AudioSetVoiceDemo";
    group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
    audio_switch_ =this->create_client<std_srvs::srv::Trigger>("audio_action_get",rmw_qos_profile_services_default, group_);

    get_voice_ = this->create_publisher<std_msgs::msg::UInt8>("volume_get", 2);
    set_voice_ = this->create_publisher<std_msgs::msg::UInt8>("volume_set", 2);
    // 使用timer触发
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(1000), std::bind(&AudioSetVoiceDemo::timer_callback, this));
  }

private:
  // 设置音量
  void SetVolume()
  {
    //音量设置为50
    uint8_t val = 15;
    std_msgs::msg::UInt8::UniquePtr volume(new std_msgs::msg::UInt8());
    volume->data = val;
    set_voice_->publish(std::move(volume));
    std::this_thread::sleep_for(std::chrono::seconds(3));
    RCLCPP_INFO(this->get_logger(), "set volume [%d]!", static_cast<int>(val));
    RCLCPP_INFO(this->get_logger(), "[%s] done!", __func__);
  }
  // 获取当前音量
  void GetVolume()
  {
    std_msgs::msg::UInt8::UniquePtr volume(new std_msgs::msg::UInt8());
    volume->data = 0;
    get_voice_->publish(std::move(volume));
    std::this_thread::sleep_for(std::chrono::seconds(3));
    RCLCPP_INFO(this->get_logger(), "[%s] done!", __func__);
  }
  void timer_callback()
  {
    if (audio_switch_ == nullptr) {
      RCLCPP_INFO(this->get_logger(), "audio switch not ready.");
    } else {
      if (!audio_switch_->wait_for_service(std::chrono::seconds(2))) {
        RCLCPP_INFO(this->get_logger(), "call switch state server not avalible");
      } else {
        std::chrono::seconds timeout(3);
        auto req = std::make_shared<std_srvs::srv::Trigger::Request>();
        auto res = audio_switch_->async_send_request(req);
        std::future_status status = res.wait_for(timeout);
        if (status != std::future_status::ready) {
          RCLCPP_INFO(this->get_logger(), "Failed to call audio switch execute services.");
          return;
        }
        RCLCPP_INFO(this->get_logger(), "get switch services res,result[%d].",res.get()->success);
        GetVolume();
        SetVolume();
        rclcpp::shutdown();
      }
    }
  }
  rclcpp::CallbackGroup::SharedPtr group_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Client<std_srvs::srv::Trigger>::SharedPtr audio_switch_ = nullptr;
  rclcpp::Publisher<std_msgs::msg::UInt8>::SharedPtr get_voice_;
  rclcpp::Publisher<std_msgs::msg::UInt8>::SharedPtr set_voice_;
  std::string name_;
};

#endif  // SET_VOICE_HPP_
