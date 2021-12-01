// Generated by gencpp from file sick_scan/SickLocStateSrv.msg
// DO NOT EDIT!


#ifndef SICK_SCAN_MESSAGE_SICKLOCSTATESRV_H
#define SICK_SCAN_MESSAGE_SICKLOCSTATESRV_H

#include <ros/service_traits.h>


#include <sick_scan/SickLocStateSrvRequest.h>
#include <sick_scan/SickLocStateSrvResponse.h>


namespace sick_scan
{

struct SickLocStateSrv
{

typedef SickLocStateSrvRequest Request;
typedef SickLocStateSrvResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SickLocStateSrv
} // namespace sick_scan


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::sick_scan::SickLocStateSrv > {
  static const char* value()
  {
    return "112e7992c0a1025af8b2c1b11d515e09";
  }

  static const char* value(const ::sick_scan::SickLocStateSrv&) { return value(); }
};

template<>
struct DataType< ::sick_scan::SickLocStateSrv > {
  static const char* value()
  {
    return "sick_scan/SickLocStateSrv";
  }

  static const char* value(const ::sick_scan::SickLocStateSrv&) { return value(); }
};


// service_traits::MD5Sum< ::sick_scan::SickLocStateSrvRequest> should match
// service_traits::MD5Sum< ::sick_scan::SickLocStateSrv >
template<>
struct MD5Sum< ::sick_scan::SickLocStateSrvRequest>
{
  static const char* value()
  {
    return MD5Sum< ::sick_scan::SickLocStateSrv >::value();
  }
  static const char* value(const ::sick_scan::SickLocStateSrvRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::sick_scan::SickLocStateSrvRequest> should match
// service_traits::DataType< ::sick_scan::SickLocStateSrv >
template<>
struct DataType< ::sick_scan::SickLocStateSrvRequest>
{
  static const char* value()
  {
    return DataType< ::sick_scan::SickLocStateSrv >::value();
  }
  static const char* value(const ::sick_scan::SickLocStateSrvRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::sick_scan::SickLocStateSrvResponse> should match
// service_traits::MD5Sum< ::sick_scan::SickLocStateSrv >
template<>
struct MD5Sum< ::sick_scan::SickLocStateSrvResponse>
{
  static const char* value()
  {
    return MD5Sum< ::sick_scan::SickLocStateSrv >::value();
  }
  static const char* value(const ::sick_scan::SickLocStateSrvResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::sick_scan::SickLocStateSrvResponse> should match
// service_traits::DataType< ::sick_scan::SickLocStateSrv >
template<>
struct DataType< ::sick_scan::SickLocStateSrvResponse>
{
  static const char* value()
  {
    return DataType< ::sick_scan::SickLocStateSrv >::value();
  }
  static const char* value(const ::sick_scan::SickLocStateSrvResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // SICK_SCAN_MESSAGE_SICKLOCSTATESRV_H