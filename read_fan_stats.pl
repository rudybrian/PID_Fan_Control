#!/usr/bin/perl
#

# Simple script to parse the PID_fan_control log file to output to snmpd.

open(FILE, "<$ARGV[0]") or die("Cannot open file: $!");

my $setpoint;
my $temp;
my $fan_speed;
@lines = reverse <FILE>;
foreach $line (@lines) {
  #print "reading line =>$line<=\n";
  my ($fan_speed_tmp) = $line =~ /(\d+)\%/i;
  if (defined $fan_speed_tmp) {
    #print "fan speed is $fan_speed_tmp\n";
    $fan_speed = $fan_speed_tmp;
  }
  my ($setpoint_tmp, $temp_tmp) = $line =~ /Setpoint: (\d+\.\d+), Temp: (\d+\.\d+),/i;
  if ($setpoint_tmp && $temp_tmp) {
    $setpoint = $setpoint_tmp;
    $temp = $temp_tmp;
    if (defined $setpoint && defined $temp && defined $fan_speed) {
      print $setpoint * 1000 . "\n" . $temp * 1000 . "\n$fan_speed\n";
      exit 0;
    } 
  }
}
