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
#ifndef SET_WAKEN_WORDS_HPP_
#define SET_WAKEN_WORDS_HPP_
#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
class AudioSetWakeUpWordsDemo : public rclcpp::Node
{
public:
  AudioSetWakeUpWordsDemo()
  : Node("AudioSetWakeUpWordsDemo")
  {
    name_ = "AudioSetWakeUpWordsDemo";
    set_wakeup_words = this->create_publisher<std_msgs::msg::String>(
      "wake_word", 2);
    // 使用timer触发
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(1000), std::bind(&AudioSetWakeUpWordsDemo::timer_callback, this));
  }

private:
  void timer_callback()
  {
    std_msgs::msg::String::UniquePtr wake_words(new std_msgs::msg::String());
    // 唤醒词
    //  wake_words->data = "铁蛋铁蛋";
    wake_words->data = "旺财旺财";
    set_wakeup_words->publish(std::move(wake_words));
    RCLCPP_INFO(this->get_logger(), "set wake up words:旺财旺财!");
    rclcpp::shutdown();
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr set_wakeup_words;

  std::string name_;
};

#endif  // SET_WAKEN_WORDS_HPP_
