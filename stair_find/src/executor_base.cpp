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

#include <memory>
#include <vector>
#include <unordered_map>
#include <string>
#include "stair_find/executor_base.hpp"
// #include "stair_find/algorithm_task_manager.hpp"
namespace cyberdog
{
namespace algorithm
{
std::unordered_map<std::string,
  std::shared_ptr<Nav2LifecyleMgrClient>> ExecutorBase::nav2_lifecycle_clients;
std::unordered_map<std::string,
  std::shared_ptr<nav2_util::LifecycleServiceClient>> ExecutorBase::lifecycle_clients;
std::unordered_map<std::string, ExecutorBase::LifecycleNodeIndexs> ExecutorBase::task_map_;
std::shared_ptr<BehaviorManager> ExecutorBase::behavior_manager_;
}  // namespace algorithm
}  // namespace cyberdog
