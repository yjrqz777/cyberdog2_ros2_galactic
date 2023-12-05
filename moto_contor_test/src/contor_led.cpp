#include <memory>
#include <string>
#include <vector>
#include "cyberdog_common/cyberdog_log.hpp"
#include "cyberdog_common/cyberdog_toml.hpp"
#include "std_srvs/srv/set_bool.hpp"
#include "skin_manager/skin_manager.hpp"
#include "elec_skin/elec_skin.hpp"
class LedContorDemo : public rclcpp::Node
{
public:
  LedContorDemo():Node("contor_led_node")
  {

  }

private:

};


int main(int argc,char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LedContorDemo>();
    // auto node = std::make_shared<AudioTalkDemo>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
