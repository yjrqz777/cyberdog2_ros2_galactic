#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "protocol/srv/audio_execute.hpp"
#include "protocol/srv/audio_text_play.hpp"
#include "protocol/msg/audio_play_extend.hpp"


int main(int argc,char ** argv )
{
    rclcpp :: init(argc,argv);                      
    auto node = std::make_shared<rclcpp::Node>("talks_node");
    RCLCPP_INFO(node->get_logger(),"talkers-----------test");
    rclcpp::spin(node);
    rclcpp::shutdown();
}





