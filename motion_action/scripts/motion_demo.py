#!/usr/bin/env python3
# Copyright (c) 2023 Beijing Xiaomi Mobile Software Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import motion_units
import time
motion_units.standup()
time.sleep(2)
motion_units.yaw(-0.35, 2000)
time.sleep(2)
motion_units.yaw(0.7, 4000)
time.sleep(4)
motion_units.yaw(-0.35,2000)
time.sleep(2)

motion_units.pitch(0.25, 2000)
time.sleep(2)
motion_units.pitch(-0.5, 4000)
time.sleep(4)
motion_units.pitch(0.25, 2000)
time.sleep(2)

motion_units.roll(0.3, 2000)
time.sleep(2)
motion_units.roll(-0.6, 4000)
time.sleep(4)
motion_units.roll(0.3, 2000)
time.sleep(10)
motion_units.getdown()
