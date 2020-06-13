iperf3_test.sh
#!/bin/bash

echo
while getopts "m:n:t:b:" arg # define all options m-mode; n-no. of terminals; t-time; b-bitrate
do
    case $arg in     # read in the input options and save the user input to the target variable
   m) mode=$OPTARG
      echo "mode (1--UDP/2--TCP):" $mode;; #save the option "mode" and print it out
    n) num_of_terminal=$OPTARG
       echo "terminals:" $num_of_terminal;; #save the option "no. of terminals" and print it out
   t) time=$OPTARG
      echo "time:" $time;;   #save the option "time" and print it out
   b) bit_rate=$OPTARG
      echo "bitrate (m--Mbps/k--Kbps):" $bit_rate;; #save the option "bitrate" and print it out
   ?) echo $arg "is not an option" exit 1;; # print warning if user input an unknown option
    esac
done

case $mode in
    1) echo "UDP: $num_of_terminal parallel streams"     # if the mode is UDP packet transmission print 
       echo "$num_of_terminal parallel streams" >> iperf_udp_1024.log  # save a notation to the log file
       ./iperf/src/iperf3 -u -c 10.51.49.182 -b $bit_rate -t $time -P $num_of_terminal >> iperf3_udp_1024.log & #iperf3 udp & save the output log to file
       echo "wait..." 
       wait
       echo "done" 
       echo " " >> iperf_udp_1024.log
       echo "UDP Transmission done" >> iperf_udp_1024.log;; #print & save some notations to the log
    2) echo "TCP: $num_of_terminal parallel streams"
       echo "$num_of_terminal parallel streams" >> iperf_tcp_1024.log
       ./iperf/src/iperf3 -c 10.51.49.182 -b $bit_rate -t $time  -P $num_of_terminal >> iperf3_tcp_1024.log & #iperf3 tcp
       echo "wait..." 
       wait
       echo "done" 
       echo " " >> iperf_tcp_1024.log
       echo "TCP Transmission done" >> iperf_tcp_1024.log;;
    ?) echo $mode "is unknown, input 1--UDP 2--TCP to choose mode" exit 1;;
    esac
