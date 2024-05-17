package main

import (
	"fmt"
	"log"
	"os"

	"github.com/PuerkitoBio/goquery"
)

func main() {
	// Open and parse each HTML file
	for i := 1; i <= 8; i++ {
		filePath := fmt.Sprintf("Exam%d.html", i)
		file, err := os.Open(filePath)
		if err != nil {
			log.Fatal(err)
		}
		defer file.Close()

		// Parse the HTML document
		doc, err := goquery.NewDocumentFromReader(file)
		if err != nil {
			log.Fatal(err)
		}

		// Extract and print each question with its corresponding answers and explanation
		doc.Find("div.result-pane--question-result-pane-wrapper--2bGiz").Each(func(index int, s *goquery.Selection) {
			// Extract and print question
			question := s.Find("div.result-pane--question-header-wrapper--3DCpC").Find("div#question-prompt p")
			fmt.Printf("Question %d:\n", index+1)
			question.Each(func(i int, p *goquery.Selection) {
				fmt.Println(p.Text())
				fmt.Println()
			})

			// Extract and print answers
			s.Find("div.result-pane--answer-result-pane--Niazi").Each(func(j int, answer *goquery.Selection) {
				fmt.Printf("Answer %d.%d:\n", index+1, j+1)
				answer.Find("div#answer-text p").Each(func(k int, p *goquery.Selection) {
					fmt.Println(p.Text())
					fmt.Println()
				})
			})

			// Extract and print explanation
			explanation := s.Find("div#overall-explanation p")
			if explanation.Length() > 0 {
				fmt.Printf("Explanation %d:\n", index+1)
				explanation.Each(func(i int, p *goquery.Selection) {
					fmt.Println(p.Text())
					fmt.Println()
				})
			}

			fmt.Println()
		})
	}
}
