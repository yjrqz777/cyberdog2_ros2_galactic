# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cyberdog_app.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63yberdog_app.proto\x12\x07grpcapi\"!\n\x0cMotionStatus\x12\x11\n\tmotion_id\x18\x01 \x01(\x05\":\n\nTaskStatus\x12\x13\n\x0btask_status\x18\x01 \x01(\x07\x12\x17\n\x0ftask_sub_status\x18\x02 \x01(\x05\"4\n\x0fSelfCheckStatus\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"0\n\x11StateSwitchStatus\x12\r\n\x05state\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\"C\n\x0e\x43hargingStatus\x12\x16\n\x0ewired_charging\x18\x01 \x01(\x08\x12\x19\n\x11wireless_charging\x18\x02 \x01(\x08\"\xe6\x02\n\x05Ticks\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x15\n\rwifi_strength\x18\x02 \x01(\x07\x12\x15\n\rbattery_power\x18\x03 \x01(\x07\x12\x10\n\x08internet\x18\x04 \x01(\x08\x12\n\n\x02sn\x18\x05 \x01(\t\x12,\n\rmotion_status\x18\x06 \x01(\x0b\x32\x15.grpcapi.MotionStatus\x12(\n\x0btask_status\x18\x07 \x01(\x0b\x32\x13.grpcapi.TaskStatus\x12\x33\n\x11self_check_status\x18\x08 \x01(\x0b\x32\x18.grpcapi.SelfCheckStatus\x12\x37\n\x13state_switch_status\x18\t \x01(\x0b\x32\x1a.grpcapi.StateSwitchStatus\x12\x30\n\x0f\x63harging_status\x18\n \x01(\x0b\x32\x17.grpcapi.ChargingStatus\x12\r\n\x05\x61udio\x18\x0b \x01(\x08\"\xb7\x10\n\x0bSendRequest\x12\x10\n\x08nameCode\x18\x01 \x01(\x07\x12\x0e\n\x06params\x18\x02 \x01(\t\"\x85\x10\n\tname_code\x12\x0b\n\x07INVALID\x10\x00\x12\x14\n\x0fGET_DEVICE_INFO\x10\xe9\x07\x12\x19\n\x14MOTION_SERVO_REQUEST\x10\xea\x07\x12\x1a\n\x15MOTION_SERVO_RESPONSE\x10\xeb\x07\x12\x17\n\x12MOTION_CMD_REQUEST\x10\xec\x07\x12\x17\n\x12\x44\x45VICE_NAME_SWITCH\x10\xf2\x07\x12\x14\n\x0f\x44\x45VICE_NAME_SET\x10\xf3\x07\x12\x16\n\x11\x44\x45VICE_VOLUME_SET\x10\xf4\x07\x12\x13\n\x0e\x44\x45VICE_MIC_SET\x10\xf5\x07\x12\x15\n\x10\x44\x45VICE_AUDIO_SET\x10\xf6\x07\x12\x17\n\x12\x41\x43\x43OUNT_MEMBER_ADD\x10\xfc\x07\x12\x1a\n\x15\x41\x43\x43OUNT_MEMBER_SEARCH\x10\xfd\x07\x12\x1a\n\x15\x41\x43\x43OUNT_MEMBER_DELETE\x10\xfe\x07\x12\x1a\n\x15\x41\x43\x43OUNT_MEMBER_CHANGE\x10\x80\x08\x12\x14\n\x0fSTOP_AUDIO_PLAY\x10\x81\x08\x12\x17\n\x12VISUAL_BACKEND_MSG\x10\xd1\x0f\x12\x18\n\x13VISUAL_FRONTEND_MSG\x10\xd2\x0f\x12!\n\x1c\x41UDIO_AUTHENTICATION_REQUEST\x10\xb9\x17\x12\"\n\x1d\x41UDIO_AUTHENTICATION_RESPONSE\x10\xba\x17\x12 \n\x1b\x41UDIO_VOICEPRINTTRAIN_START\x10\xc3\x17\x12!\n\x1c\x41UDIO_VOICEPRINTTRAIN_CANCEL\x10\xc4\x17\x12!\n\x1c\x41UDIO_VOICEPRINTTRAIN_RESULT\x10\xc5\x17\x12\x1b\n\x16\x41UDIO_VOICEPRINTS_DATA\x10\xc6\x17\x12\x1f\n\x1aIMAGE_TRANSMISSION_REQUEST\x10\xa1\x1f\x12\x13\n\x0e\x43\x41MERA_SERVICE\x10\xa2\x1f\x12 \n\x1b\x46ILES_NOT_DOWNLOAD_COMPLETE\x10\xa3\x1f\x12\x12\n\rDOWNLOAD_FILE\x10\xa4\x1f\x12\x17\n\x12OTA_STATUS_REQUEST\x10\x89\'\x12\x1e\n\x19OTA_VERSION_QUERY_REQUEST\x10\x8a\'\x12\x1f\n\x1aOTA_START_DOWNLOAD_REQUEST\x10\x8b\'\x12\x1e\n\x19OTA_START_UPGRADE_REQUEST\x10\x8c\'\x12\x1e\n\x19OTA_PROCESS_QUERY_REQUEST\x10\x8d\'\x12&\n!OTA_ESTIMATE_UPGRADE_TIME_REQUEST\x10\x8e\'\x12\x12\n\rOTA_NX_REBOOT\x10\x8f\'\x12\x15\n\x10OTA_ACTION_START\x10\x92\'\x12\x18\n\x13OTA_ACTION_CONTINUE\x10\x93\'\x12\x15\n\x10MAP_DATA_REQUEST\x10\xf1.\x12\x1a\n\x15MAP_SET_LABLE_REQUEST\x10\xf2.\x12\x1a\n\x15MAP_GET_LABLE_REQUEST\x10\xf3.\x12\x0f\n\nNAV_ACTION\x10\xf4.\x12\x19\n\x14MAP_DOG_POSE_REQUEST\x10\xf5.\x12\x12\n\rNAV_PLAN_PATH\x10\xf6.\x12\x11\n\x0cTRACKING_OBJ\x10\xf7.\x12\x1a\n\x15SELECTED_TRACKING_OBJ\x10\xf8.\x12\x14\n\x0fSTOP_NAV_ACTION\x10\xf9.\x12\x16\n\x11\x41\x43\x43\x45SS_NAV_ACTION\x10\xfa.\x12\x0f\n\nLASER_SCAN\x10\xfb.\x12\x17\n\x12\x45NABLE_POINT_CLOUD\x10\xfc.\x12\x16\n\x11POINT_CLOUD_STATE\x10\xfd.\x12\x17\n\x12\x46\x41\x43\x45_ENTRY_REQUEST\x10\xd9\x36\x12\x1b\n\x16\x46\x41\x43\x45_RECORDING_REQUEST\x10\xda\x36\x12\x1e\n\x19\x46\x41\x43\x45_ENTRY_RESULT_PUBLISH\x10\xdb\x36\x12$\n\x1f\x46\x41\x43\x45_RECOGNITION_RESULT_PUBLISH\x10\xdc\x36\x12\x13\n\x0e\x42LUETOOTH_SCAN\x10\xc1>\x12\x16\n\x11\x42LUETOOTH_CONNECT\x10\xc2>\x12&\n!BLUETOOTH_DISCONNECTED_UNEXPECTED\x10\xc3>\x12 \n\x1b\x42LUETOOTH_CONNECTED_DEVICES\x10\xc4>\x12 \n\x1b\x42LE_DIVICE_FIRMWARE_VERSION\x10\xc5>\x12\x1d\n\x18\x42LE_DEVICE_BATTERY_LEVEL\x10\xc6>\x12\x17\n\x12\x44\x45LETE_BLE_HISTORY\x10\xc7>\x12%\n BLE_FIRMWARE_UPDATE_NOTIFICATION\x10\xc8>\x12\x18\n\x13UPDATE_BLE_FIRMWARE\x10\xc9>\x12\x15\n\x10\x42LE_DFU_PROGRESS\x10\xca>\x12\x11\n\x0cSET_BT_TREAD\x10\xcb>\x12\x14\n\x0fUPDATE_BT_TREAD\x10\xcc>\x12\x11\n\x0cGET_BT_TREAD\x10\xcd>\x12\x1a\n\x15UNLOCK_DEVELOP_ACCESS\x10\xc6\x46\x12\x13\n\x0eREBOOT_MACHINE\x10\xc7\x46\x12\x13\n\x0eSTATUS_REQUEST\x10\x91N\x12\x13\n\x0eLOW_POWER_EXIT\x10\x92N\x12\x1a\n\x15\x41UTO_LOW_POWER_ENABLE\x10\x93N\x12\x19\n\x14SET_WORK_ENVIRONMENT\x10\x94N\x12\x12\n\rUPLOAD_SYSLOG\x10\x95N\x12\x0e\n\tPOWER_OFF\x10\x96N\x12\x13\n\x0eLCM_LOG_UPLOAD\x10\x97N\x12\x15\n\x10\x45NABLE_ELEC_SKIN\x10\xf9U\x12\x12\n\rSET_ELEC_SKIN\x10\xfaU\x12\x18\n\x13\x44OG_LEG_CALIBRATION\x10\xe1]\"-\n\x0bRecResponse\x12\x10\n\x08nameCode\x18\x01 \x01(\x07\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"\x18\n\x06Result\x12\x0e\n\x06result\x18\x01 \x01(\t\"U\n\tFileChunk\x12\x12\n\nerror_code\x18\x01 \x01(\x07\x12\x11\n\tfile_name\x18\x02 \x01(\t\x12\x11\n\tfile_size\x18\x03 \x01(\x07\x12\x0e\n\x06\x62uffer\x18\x04 \x01(\x0c\x32\xad\x01\n\x07GrpcApp\x12\x39\n\x07sendMsg\x12\x14.grpcapi.SendRequest\x1a\x14.grpcapi.RecResponse\"\x00\x30\x01\x12.\n\theartbeat\x12\x0e.grpcapi.Ticks\x1a\x0f.grpcapi.Result\"\x00\x12\x37\n\x07getFile\x12\x14.grpcapi.SendRequest\x1a\x12.grpcapi.FileChunk\"\x00\x30\x01\x42/\n\x13io.grpc.cyberdogappB\x10\x43yberdogAppProtoP\x01\xa2\x02\x03RTGb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cyberdog_app_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023io.grpc.cyberdogappB\020CyberdogAppProtoP\001\242\002\003RTG'
  _globals['_MOTIONSTATUS']._serialized_start=31
  _globals['_MOTIONSTATUS']._serialized_end=64
  _globals['_TASKSTATUS']._serialized_start=66
  _globals['_TASKSTATUS']._serialized_end=124
  _globals['_SELFCHECKSTATUS']._serialized_start=126
  _globals['_SELFCHECKSTATUS']._serialized_end=178
  _globals['_STATESWITCHSTATUS']._serialized_start=180
  _globals['_STATESWITCHSTATUS']._serialized_end=228
  _globals['_CHARGINGSTATUS']._serialized_start=230
  _globals['_CHARGINGSTATUS']._serialized_end=297
  _globals['_TICKS']._serialized_start=300
  _globals['_TICKS']._serialized_end=658
  _globals['_SENDREQUEST']._serialized_start=661
  _globals['_SENDREQUEST']._serialized_end=2764
  _globals['_SENDREQUEST_NAME_CODE']._serialized_start=711
  _globals['_SENDREQUEST_NAME_CODE']._serialized_end=2764
  _globals['_RECRESPONSE']._serialized_start=2766
  _globals['_RECRESPONSE']._serialized_end=2811
  _globals['_RESULT']._serialized_start=2813
  _globals['_RESULT']._serialized_end=2837
  _globals['_FILECHUNK']._serialized_start=2839
  _globals['_FILECHUNK']._serialized_end=2924
  _globals['_GRPCAPP']._serialized_start=2927
  _globals['_GRPCAPP']._serialized_end=3100
# @@protoc_insertion_point(module_scope)
