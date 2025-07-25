package main

import (
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"

	"github.com/buger/jsonparser"
)

func createHandler(w http.ResponseWriter, r *http.Request) {
	uuid := r.FormValue("uuid")
	root_perm := r.FormValue("root_perm")
	if uuid == "" {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	filePath := filepath.Join("/app/data", uuid+".json")
	file, _ := os.Create(filePath)
	defer file.Close()
	file.WriteString(root_perm)
	w.WriteHeader(http.StatusOK)
}

func flag(w http.ResponseWriter, r *http.Request) {
	uuid := r.URL.Query().Get("uuid")
	filePath := filepath.Join("/app/data", uuid+".json")
	fileContent, err := ioutil.ReadFile(filePath)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	value, _ := jsonparser.GetInt(fileContent, "root")
	w.Header().Set("Content-Type", "application/json")
	if value == 0 {
		flag := os.Getenv("FLAG")
		w.Write([]byte(`{"flag":"` + flag + `"}`))
	} else {
		w.Write([]byte(`{"flag":no flag for you}`))
	}
}

func main() {
	os.MkdirAll("/app/data", 0755)
	http.HandleFunc("/create", createHandler)
	http.HandleFunc("/flag", flag)
	http.ListenAndServe(":5000", nil)
}
