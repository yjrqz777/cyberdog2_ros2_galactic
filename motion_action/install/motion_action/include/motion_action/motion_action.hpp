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
#ifndef MOTION_ACTION__MOTION_ACTION_HPP_
#define MOTION_ACTION__MOTION_ACTION_HPP_
#include <unistd.h>
#include <lcm/lcm-cpp.hpp>
#include <string>
#include <thread>
#include <chrono>
#include <functional>
#include <iostream>
#include <memory>
#include <map>
#include <vector>
#include <mutex>
#include "protocol/msg/motion_servo_cmd.hpp"
#include "protocol/srv/motion_result_cmd.hpp"
#include "protocol/msg/motion_status.hpp"
#include "protocol/msg/motion_servo_response.hpp"
#include "protocol/lcm/robot_control_response_lcmt.hpp"
#include "protocol/lcm/robot_control_cmd_lcmt.hpp"
#include "protocol/lcm/state_estimator_lcmt.hpp"
#include "cyberdog_common/cyberdog_log.hpp"
#include "cyberdog_common/cyberdog_toml.hpp"
#include "motion_action/motion_macros.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include "ament_index_cpp/get_package_prefix.hpp"
// #include "elec_skin/elec_skin_base.hpp"
#include "skin_manager/skin_manager.hpp"

namespace cyberdog
{
namespace motion
{

struct MotionIdMap
{
  std::vector<int32_t> map;
  std::vector<int32_t> pre_motion;
  std::vector<int32_t> post_motion;
  int32_t min_exec_time;
};  // struct MotionIdMap

inline bool CompareLcmResponse(const LcmResponse & res1, const LcmResponse & res2)
{
  bool flag = true;
  for (uint8_t i = 0; i < 12; ++i) {
    flag &= (res1.motor_error[i] == res2.motor_error[i]);
  }
  return res1.mode == res2.mode &&
         res1.gait_id == res2.gait_id &&
         res1.contact == res2.contact &&
         res1.order_process_bar == res2.order_process_bar &&
         res1.switch_status == res2.switch_status &&
         res1.ori_error == res2.ori_error &&
         res1.footpos_error == res2.footpos_error &&
         res1.motor_error && flag;
}
class MotionAction final
{
public:
  MotionAction();
  ~MotionAction();

public:
  void Execute(const MotionServoCmdMsg::SharedPtr msg);
  void Execute(const MotionResultSrv::Request::SharedPtr request);
  void Execute(const MotionSequenceShowSrv::Request::SharedPtr request);
  void Execute(const MotionQueueCustomSrv::Request::SharedPtr request);
  void Execute(const robot_control_cmd_lcmt & lcm);
  void RegisterFeedback(std::function<void(MotionStatusMsg::SharedPtr)> feedback);
  void RegisterTomlLog(std::function<void(const robot_control_cmd_lcmt &)> toml_log);
  bool Init(
    const std::string & publish_url = kLCMActionPublishURL,
    const std::string & subscribe_url = kLCMActionSubscibeURL);
  bool SelfCheck();
  std::map<int32_t, MotionIdMap> GetMotionIdMap() {return motion_id_map_;}
  bool SequenceDefImpl(const std::string & toml_data);
  void ShowDebugLog(bool show) {show_ = show;}
  // void ShowDefaultSkin(bool default_color, bool align_contact)
  // {
  //   INFO("ShowDefaultSkin");
  //   align_contact_ = align_contact;
  //   PositionColorChangeDirection dir;
  //   dir = default_color ? change_dir_.front() : change_dir_.back();
  //   for (auto leg : leg_map) {
  //     for (auto p : leg.second) {
  //       elec_skin_->PositionContril(
  //         p,
  //         dir,
  //         start_dir_,
  //         gradual_duration_);
  //     }
  //   }
  // }
  // void ShowStandElecSkin()
  // {
  //   INFO("ShowStandElecSkin");
  //   align_contact_ = false;
  //   elec_skin_->ModelControl(ModelSwitch::MS_WAVEF, stand_gradual_duration_);
  // }
  // void ShowTwinkElecSkin()
  // {
  //   INFO("ShowTwinkElecSkin");
  //   align_contact_ = false;
  //   elec_skin_->ModelControl(ModelSwitch::MS_FLASH, twink_gradual_duration_);
  // }
  // void ShowRandomElecSkin()
  // {
  //   INFO("ShowRandomElecSkin");
  //   align_contact_ = false;
  //   elec_skin_->ModelControl(ModelSwitch::MS_RANDOM, random_gradual_duration_);
  // }
  // void SetAlignContact(bool align_contact)
  // {
  //   align_contact_ = align_contact;
  // }
  void ShowBlackSkin()
  {
    bool enable = elec_skin_manager_->GetEnableStatus();
    if (!enable) {
      return;
    }
    elec_skin_manager_->SetAlignContact(false);
    elec_skin_manager_->ShowBlackElecSkin(gradual_duration_);
  }

  void ShowWhiteSkin()
  {
    bool enable = elec_skin_manager_->GetEnableStatus();
    if (!enable) {
      return;
    }
    elec_skin_manager_->SetAlignContact(true);
    elec_skin_manager_->ShowWhiteElecSkin(gradual_duration_);
  }

  void SetState(const MotionMgrState & state)
  {
    state_ = state;
  }

private:
  void WriteLcm();
  void ReadActionResponseLcm(
    const lcm::ReceiveBuffer *, const std::string &,
    const robot_control_response_lcmt * msg);
  void ReadSeqDefResultLcm(
    const lcm::ReceiveBuffer *, const std::string &,
    const file_recv_lcmt * msg);
  void ReadStateEstimatorLcm(
    const lcm::ReceiveBuffer *, const std::string &,
    const state_estimator_lcmt * msg);
  bool ParseMotionIdMap();
  // bool ParseElecSkin();

private:
  std::thread control_thread_, response_thread_;
  std::function<void(MotionStatusMsg::SharedPtr)> feedback_func_;
  std::function<void(const robot_control_cmd_lcmt &)> toml_log_func_;
  std::shared_ptr<lcm::LCM> lcm_publish_instance_, lcm_subscribe_instance_;
  std::shared_ptr<lcm::LCM> lcm_recv_subscribe_instance_;
  std::shared_ptr<lcm::LCM> lcm_state_estimator_subscribe_instance_;
  // std::shared_ptr<ElecSkinBase> elec_skin_{nullptr};
  std::shared_ptr<SkinManagerNode> elec_skin_manager_{nullptr};
  // std::unordered_map<uint8_t, std::vector<PositionSkin>> leg_map;
  std::mutex lcm_write_mutex_;
  std::mutex seq_def_result_mutex_;
  std::condition_variable seq_def_result_cv_;
  robot_control_cmd_lcmt lcm_cmd_;
  std::map<int32_t, MotionIdMap> motion_id_map_;
  // std::vector<PositionColorChangeDirection> change_dir_;
  // PositionColorStartDirection start_dir_;
  MotionMgrState state_;
  int32_t last_motion_id_{0};
  int32_t gradual_duration_{50};
  // int32_t stand_gradual_duration_{0};
  // int32_t twink_gradual_duration_{0};
  // int32_t random_gradual_duration_{0};
  uint8_t lcm_publish_duration_;
  int8_t last_res_mode_{0}, last_res_gait_id_{0};
  int8_t life_count_{0};
  bool lcm_cmd_init_{false}, ins_init_{false};
  bool sequence_recv_result_{false}, sequence_def_result_waiting_{false};
  bool show_{false};
  // bool align_contact_{true};
  bool lcm_ready_{false};
  LOGGER_MINOR_INSTANCE("MotionAction");
};  // class MotionAction
}  // namespace motion
}  // namespace cyberdog
#endif  // MOTION_ACTION__MOTION_ACTION_HPP_
