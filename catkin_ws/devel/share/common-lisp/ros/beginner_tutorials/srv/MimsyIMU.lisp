; Auto-generated. Do not edit!


(cl:in-package beginner_tutorials-srv)


;//! \htmlinclude MimsyIMU-request.msg.html

(cl:defclass <MimsyIMU-request> (roslisp-msg-protocol:ros-message)
  ((accelx
    :reader accelx
    :initarg :accelx
    :type cl:integer
    :initform 0)
   (mote_ip
    :reader mote_ip
    :initarg :mote_ip
    :type cl:string
    :initform ""))
)

(cl:defclass MimsyIMU-request (<MimsyIMU-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MimsyIMU-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MimsyIMU-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name beginner_tutorials-srv:<MimsyIMU-request> is deprecated: use beginner_tutorials-srv:MimsyIMU-request instead.")))

(cl:ensure-generic-function 'accelx-val :lambda-list '(m))
(cl:defmethod accelx-val ((m <MimsyIMU-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beginner_tutorials-srv:accelx-val is deprecated.  Use beginner_tutorials-srv:accelx instead.")
  (accelx m))

(cl:ensure-generic-function 'mote_ip-val :lambda-list '(m))
(cl:defmethod mote_ip-val ((m <MimsyIMU-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beginner_tutorials-srv:mote_ip-val is deprecated.  Use beginner_tutorials-srv:mote_ip instead.")
  (mote_ip m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MimsyIMU-request>) ostream)
  "Serializes a message object of type '<MimsyIMU-request>"
  (cl:let* ((signed (cl:slot-value msg 'accelx)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'mote_ip))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'mote_ip))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MimsyIMU-request>) istream)
  "Deserializes a message object of type '<MimsyIMU-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'accelx) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mote_ip) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'mote_ip) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MimsyIMU-request>)))
  "Returns string type for a service object of type '<MimsyIMU-request>"
  "beginner_tutorials/MimsyIMURequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MimsyIMU-request)))
  "Returns string type for a service object of type 'MimsyIMU-request"
  "beginner_tutorials/MimsyIMURequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MimsyIMU-request>)))
  "Returns md5sum for a message object of type '<MimsyIMU-request>"
  "c31e1566ea5c48673b33eed78f22421a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MimsyIMU-request)))
  "Returns md5sum for a message object of type 'MimsyIMU-request"
  "c31e1566ea5c48673b33eed78f22421a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MimsyIMU-request>)))
  "Returns full string definition for message of type '<MimsyIMU-request>"
  (cl:format cl:nil "int64 accelx~%string mote_ip~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MimsyIMU-request)))
  "Returns full string definition for message of type 'MimsyIMU-request"
  (cl:format cl:nil "int64 accelx~%string mote_ip~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MimsyIMU-request>))
  (cl:+ 0
     8
     4 (cl:length (cl:slot-value msg 'mote_ip))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MimsyIMU-request>))
  "Converts a ROS message object to a list"
  (cl:list 'MimsyIMU-request
    (cl:cons ':accelx (accelx msg))
    (cl:cons ':mote_ip (mote_ip msg))
))
;//! \htmlinclude MimsyIMU-response.msg.html

(cl:defclass <MimsyIMU-response> (roslisp-msg-protocol:ros-message)
  ((response
    :reader response
    :initarg :response
    :type cl:string
    :initform ""))
)

(cl:defclass MimsyIMU-response (<MimsyIMU-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MimsyIMU-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MimsyIMU-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name beginner_tutorials-srv:<MimsyIMU-response> is deprecated: use beginner_tutorials-srv:MimsyIMU-response instead.")))

(cl:ensure-generic-function 'response-val :lambda-list '(m))
(cl:defmethod response-val ((m <MimsyIMU-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beginner_tutorials-srv:response-val is deprecated.  Use beginner_tutorials-srv:response instead.")
  (response m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MimsyIMU-response>) ostream)
  "Serializes a message object of type '<MimsyIMU-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'response))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'response))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MimsyIMU-response>) istream)
  "Deserializes a message object of type '<MimsyIMU-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'response) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'response) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MimsyIMU-response>)))
  "Returns string type for a service object of type '<MimsyIMU-response>"
  "beginner_tutorials/MimsyIMUResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MimsyIMU-response)))
  "Returns string type for a service object of type 'MimsyIMU-response"
  "beginner_tutorials/MimsyIMUResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MimsyIMU-response>)))
  "Returns md5sum for a message object of type '<MimsyIMU-response>"
  "c31e1566ea5c48673b33eed78f22421a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MimsyIMU-response)))
  "Returns md5sum for a message object of type 'MimsyIMU-response"
  "c31e1566ea5c48673b33eed78f22421a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MimsyIMU-response>)))
  "Returns full string definition for message of type '<MimsyIMU-response>"
  (cl:format cl:nil "string response~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MimsyIMU-response)))
  "Returns full string definition for message of type 'MimsyIMU-response"
  (cl:format cl:nil "string response~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MimsyIMU-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'response))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MimsyIMU-response>))
  "Converts a ROS message object to a list"
  (cl:list 'MimsyIMU-response
    (cl:cons ':response (response msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'MimsyIMU)))
  'MimsyIMU-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'MimsyIMU)))
  'MimsyIMU-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MimsyIMU)))
  "Returns string type for a service object of type '<MimsyIMU>"
  "beginner_tutorials/MimsyIMU")