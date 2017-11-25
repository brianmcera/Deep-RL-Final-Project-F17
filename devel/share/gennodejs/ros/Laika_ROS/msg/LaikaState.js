// Auto-generated. Do not edit!

// (in-package Laika_ROS.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class LaikaState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.body_id = null;
      this.position = null;
      this.orientation = null;
      this.lin_vel = null;
      this.ang_vel = null;
    }
    else {
      if (initObj.hasOwnProperty('body_id')) {
        this.body_id = initObj.body_id
      }
      else {
        this.body_id = 0;
      }
      if (initObj.hasOwnProperty('position')) {
        this.position = initObj.position
      }
      else {
        this.position = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('orientation')) {
        this.orientation = initObj.orientation
      }
      else {
        this.orientation = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('lin_vel')) {
        this.lin_vel = initObj.lin_vel
      }
      else {
        this.lin_vel = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('ang_vel')) {
        this.ang_vel = initObj.ang_vel
      }
      else {
        this.ang_vel = new geometry_msgs.msg.Point();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LaikaState
    // Serialize message field [body_id]
    bufferOffset = _serializer.uint32(obj.body_id, buffer, bufferOffset);
    // Serialize message field [position]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.position, buffer, bufferOffset);
    // Serialize message field [orientation]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.orientation, buffer, bufferOffset);
    // Serialize message field [lin_vel]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.lin_vel, buffer, bufferOffset);
    // Serialize message field [ang_vel]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.ang_vel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LaikaState
    let len;
    let data = new LaikaState(null);
    // Deserialize message field [body_id]
    data.body_id = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [position]
    data.position = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [orientation]
    data.orientation = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [lin_vel]
    data.lin_vel = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [ang_vel]
    data.ang_vel = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 100;
  }

  static datatype() {
    // Returns string type for a message object
    return 'Laika_ROS/LaikaState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c9eae5e56960b9b108fffef42a77bc21';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    const resolved = new LaikaState(null);
    if (msg.body_id !== undefined) {
      resolved.body_id = msg.body_id;
    }
    else {
      resolved.body_id = 0
    }

    if (msg.position !== undefined) {
      resolved.position = geometry_msgs.msg.Point.Resolve(msg.position)
    }
    else {
      resolved.position = new geometry_msgs.msg.Point()
    }

    if (msg.orientation !== undefined) {
      resolved.orientation = geometry_msgs.msg.Point.Resolve(msg.orientation)
    }
    else {
      resolved.orientation = new geometry_msgs.msg.Point()
    }

    if (msg.lin_vel !== undefined) {
      resolved.lin_vel = geometry_msgs.msg.Point.Resolve(msg.lin_vel)
    }
    else {
      resolved.lin_vel = new geometry_msgs.msg.Point()
    }

    if (msg.ang_vel !== undefined) {
      resolved.ang_vel = geometry_msgs.msg.Point.Resolve(msg.ang_vel)
    }
    else {
      resolved.ang_vel = new geometry_msgs.msg.Point()
    }

    return resolved;
    }
};

module.exports = LaikaState;
