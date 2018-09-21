# LAB 1 

Protect program from unauthorised access using CPUID check. This program should be done in two parts: first is the installer which contains license calculating, the second part is the "program" itself, which is basically a sum check.

./installer binary generates a license file based on md5 hash of /proc/cpuinfo (system-profiler in macOS case) which is to be placed into the same directory with the ./program binary.

./program binary generates the current cpuinfo md5 hash and compares it with the same of the file.