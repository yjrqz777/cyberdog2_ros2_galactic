#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "cyberdog_common/cyberdog_log.hpp"
#include "cyberdog_debug/backtrace.hpp"

#include "stair_find/stair_find.hpp"
#include "stair_find/executor_base.hpp"

// #include "stair_find/algorithm_task_manager.hpp"

// using namespace cyberdog::algorithm;  

int main(int argc, char ** argv)
{
  // LOGGER_MAIN_INSTANCE("AlgorithmTaskManager");
  // cyberdog::debug::register_signal();
  rclcpp::init(argc, argv);
  auto atm_ptr = std::make_shared<cyberdog::algorithm::ExecutorStairFind>("test");
  // if (!atm_ptr->Start()) {
  //   ERROR("Init failed, will exit with error!");
  //   return -1;
  // }
  // atm_ptr->Run();
  return 0;
}
