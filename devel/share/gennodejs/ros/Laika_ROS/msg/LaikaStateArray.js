// Auto-generated. Do not edit!

// (in-package Laika_ROS.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let LaikaState = require('./LaikaState.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class LaikaStateArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.states = null;
      this.cable_rl = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('states')) {
        this.states = initObj.states
      }
      else {
        this.states = [];
      }
      if (initObj.hasOwnProperty('cable_rl')) {
        this.cable_rl = initObj.cable_rl
      }
      else {
        this.cable_rl = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LaikaStateArray
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [states]
    // Serialize the length for message field [states]
    bufferOffset = _serializer.uint32(obj.states.length, buffer, bufferOffset);
    obj.states.forEach((val) => {
      bufferOffset = LaikaState.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [cable_rl]
    bufferOffset = _arraySerializer.float32(obj.cable_rl, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LaikaStateArray
    let len;
    let data = new LaikaStateArray(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [states]
    // Deserialize array length for message field [states]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.states = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.states[i] = LaikaState.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [cable_rl]
    data.cable_rl = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 100 * object.states.length;
    length += 4 * object.cable_rl.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'Laika_ROS/LaikaStateArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e19ca31cf4a3cbb12d873eb3d8084a5d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    LaikaState[] states
    float32[] cable_rl
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    # 0: no frame
    # 1: global frame
    string frame_id
    
    ================================================================================
    MSG: Laika_ROS/LaikaState
    uint32 body_id
    geometry_msgs/Point position
    geometry_msgs/Point orientation
    geometry_msgs/Point lin_vel
    geometry_msgs/Point ang_vel
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new LaikaStateArray(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.states !== undefined) {
      resolved.states = new Array(msg.states.length);
      for (let i = 0; i < resolved.states.length; ++i) {
        resolved.states[i] = LaikaState.Resolve(msg.states[i]);
      }
    }
    else {
      resolved.states = []
    }

    if (msg.cable_rl !== undefined) {
      resolved.cable_rl = msg.cable_rl;
    }
    else {
      resolved.cable_rl = []
    }

    return resolved;
    }
};

module.exports = LaikaStateArray;
