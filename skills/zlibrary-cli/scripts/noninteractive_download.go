package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/heartleo/zlib"
)

type session struct {
	Cookies map[string]string `json:"cookies"`
	Domain  string            `json:"domain"`
}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: noninteractive_download BOOK_ID DEST_DIR")
		os.Exit(2)
	}

	bookID := os.Args[1]
	destDir := os.Args[2]

	home, err := os.UserHomeDir()
	if err != nil {
		panic(err)
	}
	data, err := os.ReadFile(filepath.Join(home, ".config", "zlib", "session.json"))
	if err != nil {
		panic(err)
	}

	var s session
	if err := json.Unmarshal(data, &s); err != nil {
		panic(err)
	}

	c := zlib.NewClient()
	if s.Domain != "" {
		c.SetDomain(s.Domain)
	}
	c.SetCookies(s.Cookies)

	book, err := c.FetchBook(bookID)
	if err != nil {
		panic(fmt.Errorf("fetch book: %w", err))
	}
	if book.DownloadURL == "" {
		panic("empty download URL")
	}

	res, err := c.Download(book.DownloadURL, destDir, nil)
	if err != nil {
		panic(fmt.Errorf("download: %w", err))
	}
	fmt.Printf("%s\n%d\n", res.FilePath, res.Size)
}
