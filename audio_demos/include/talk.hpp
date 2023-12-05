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
#ifndef TALK_HPP_
#define TALK_HPP_
#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "protocol/srv/audio_execute.hpp"
#include "protocol/srv/audio_text_play.hpp"
#include "protocol/msg/audio_play_extend.hpp"

class AudioTalkDemo : public rclcpp::Node
{
public:
  AudioTalkDemo():Node("AudioTalkDemo")
  {
    name_ = "AudioTalkDemo";
    group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
    audio_client_ = this->create_client<protocol::srv::AudioExecute>("get_audio_state",rmw_qos_profile_services_default, group_);

    audio_text_speech_client_ =this->create_client<protocol::srv::AudioTextPlay>("speech_text_play",rmw_qos_profile_services_default, group_);

    speech_play_extend_ = this->create_publisher<protocol::msg::AudioPlayExtend>("speech_play_extend", 2);
    // 使用timer触发
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(1000), std::bind(&AudioTalkDemo::timer_callback, this));
  }

private:
  // 使用topic触发语音播报
  void RosTopicTalk(bool online)
  {
    protocol::msg::AudioPlayExtend::UniquePtr speech_play_extend_voice(new protocol::msg::
      AudioPlayExtend());
    speech_play_extend_voice->module_name = name_;
    speech_play_extend_voice->is_online = online;
    speech_play_extend_voice->speech.module_name = name_;
    speech_play_extend_voice->speech.play_id = 32;  // please close to me.
    speech_play_extend_voice->text = "这是在线语音32,this is online voice.";
    speech_play_extend_->publish(std::move(speech_play_extend_voice));
    std::this_thread::sleep_for(std::chrono::seconds(5));
    RCLCPP_INFO(this->get_logger(), "[%s] done!", __func__);
  }
  // 使用service触发语音播报
  void RosServiceTalk(bool online)
  {
    if (!audio_text_speech_client_->wait_for_service(std::chrono::seconds(2))) {
      RCLCPP_INFO(this->get_logger(), "[%s] server not avalible!", __func__);
    } else {
      std::chrono::seconds timeout(10);
      auto req = std::make_shared<protocol::srv::AudioTextPlay::Request>();
      req->module_name = name_;
      req->is_online = online;
      req->speech.module_name = name_;
      req->speech.play_id = 33;  // please leave me alone.
      req->text = "这是在线语音33,this is online voice.";
      auto res = audio_text_speech_client_->async_send_request(req);
      std::future_status status = res.wait_for(timeout);
      if (status != std::future_status::ready) {
        RCLCPP_INFO(this->get_logger(), "[%s] Failed to call audio speech services.", __func__);
        return;
      }
      if (!res.get()->status) {
        RCLCPP_INFO(this->get_logger(), "[%s] speech play text online success!", __func__);
      } else {
        RCLCPP_INFO(this->get_logger(), "[%s] speech play text online failed!", __func__);
      }
    }
  }
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
        auto res = audio_client_->async_send_request(req);
        std::future_status status = res.wait_for(timeout);
        if (status != std::future_status::ready) {
          RCLCPP_INFO(this->get_logger(), "Failed to call audio execute services.");
          return;
        }
        RCLCPP_INFO(
          this->get_logger(), "get audio services res,result[%d],code[%d].",
          res.get()->result, res.get()->code);
        if (res.get()->result) {
          /*offline voice*/
          //   RosServiceTalk(false);
          //   RosTopicTalk(false);
          /*online voice*/
          RosServiceTalk(true);
          RosTopicTalk(true);
          rclcpp::shutdown();
        } else {
          RCLCPP_INFO(this->get_logger(), "audio is not ready");
        }
      }
    }
  }
  rclcpp::CallbackGroup::SharedPtr group_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Client<protocol::srv::AudioExecute>::SharedPtr audio_client_ = nullptr;
  rclcpp::Client<protocol::srv::AudioTextPlay>::SharedPtr audio_text_speech_client_ = nullptr;
  rclcpp::Publisher<protocol::msg::AudioPlayExtend>::SharedPtr speech_play_extend_;

  std::string name_;
};

#endif  // TALK_HPP_
