#include <chrono>
#include <string>
#include <memory>
#include <utility>
#include "rclcpp/rclcpp.hpp"
#include "protocol/srv/audio_execute.hpp"
#include "protocol/srv/audio_text_play.hpp"
#include "protocol/msg/audio_play_extend.hpp"
#include "std_srvs/srv/trigger.hpp"
#include "std_msgs/msg/u_int8.hpp"


class talkersNode : public rclcpp::Node
{
private:
    std::string name_;
    rclcpp::CallbackGroup::SharedPtr group_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<protocol::srv::AudioExecute>::SharedPtr audio_client_ = nullptr;

    rclcpp::Publisher<protocol::msg::AudioPlayExtend>::SharedPtr speech_play_extend_;
    rclcpp::Publisher<std_msgs::msg::UInt8>::SharedPtr set_voice_;

    void talk_topic(bool online,std::__cxx11::string strs)
    {
        protocol::msg::AudioPlayExtend::UniquePtr speech_play_extend_voice(new protocol::msg::AudioPlayExtend());
        speech_play_extend_voice->module_name = name_;
        speech_play_extend_voice->is_online = online;
        speech_play_extend_voice->speech.module_name = name_;
        speech_play_extend_voice->speech.play_id = 32;  // please close to me.
        speech_play_extend_voice->text = strs;
        speech_play_extend_->publish(std::move(speech_play_extend_voice));
        // std::this_thread::sleep_for(std::chrono::seconds(5));
        RCLCPP_INFO(this->get_logger(), "[%s] done!", __func__);
    }

    void timer_callback()
    {
        //音量设置为50
        // uint8_t val = 25;
        // std_msgs::msg::UInt8::UniquePtr volume(new std_msgs::msg::UInt8());
        // volume->data = val;
        // set_voice_->publish(std::move(volume));
        // std::this_thread::sleep_for(std::chrono::seconds(3));
        // RCLCPP_INFO(this->get_logger(), "set volume [%d]!", static_cast<int>(val));
        // RCLCPP_INFO(this->get_logger(), "[%s] done!", __func__);

        RCLCPP_WARN(this->get_logger(), "audio client %d,---%s---",audio_client_);

        if(audio_client_ == nullptr)
        {
            RCLCPP_WARN(this->get_logger(), "audio client not ready.");
        }
         
        talk_topic(false,"你好啊，再见 , place,go,study");

        RCLCPP_INFO(this->get_logger(),"-----time:i=%d---------",i);
        i++;
    }
public:
    int i=0;
    talkersNode(std::string name ):Node(name)
    {
        name_ = "AudioTalkDemo";
        group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
        audio_client_ = this->create_client<protocol::srv::AudioExecute>("get_audio_state",rmw_qos_profile_services_default, group_);
        RCLCPP_INFO(this->get_logger(),"talkers---------%s",name.c_str());
        timer_ =this->create_wall_timer(std::chrono::milliseconds(5000),std::bind(&talkersNode::timer_callback, this));
        speech_play_extend_ = this->create_publisher<protocol::msg::AudioPlayExtend>("speech_play_extend",2);
        set_voice_ = this->create_publisher<std_msgs::msg::UInt8>("volume_set", 2);
    };

};



int main(int argc,char ** argv )
{
    rclcpp :: init(argc,argv);                      
    auto node = std::make_shared<talkersNode>("talks_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
}





