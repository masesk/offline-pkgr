package main

import (
	"compress/gzip" // Add this import
	"fmt"
	"io"
	"log"
	"os"
	"bufio"
	"os/exec"
	"path/filepath"
	"archive/tar"
	"gopkg.in/ini.v1"
)

type GenericInstaller struct{}

func (gi *GenericInstaller) Install(tarFilePath string) error {
	// Extract tar.gz file
	err := extractTarGz(tarFilePath, "/tmp/")
	if err != nil {
		return err
	}

	// Read config file
	cfg, err := ini.Load("/tmp/install.ini")
	if err != nil {
		return err
	}

	installCommand := cfg.Section("install").Key("install_command").String()
	directory := cfg.Section("install").Key("directory").String()

	// Change directory
	err = os.Chdir(directory)
	if err != nil {
		return os.RemoveAll(directory)
	}

	fmt.Println("Executing: ", installCommand)
	cmd := exec.Command("/bin/sh", "-c", installCommand)

	// Set up pipes for stdout and stderr
	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating stdout pipe: %v\n", err)
		return os.RemoveAll(directory)
	}
	stderrPipe, err := cmd.StderrPipe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating stderr pipe: %v\n", err)
		return os.RemoveAll(directory)
	}

	// Start the command
	if err := cmd.Start(); err != nil {
		fmt.Fprintf(os.Stderr, "Error starting command: %v\n", err)
		return os.RemoveAll(directory)
	}

	// Function to stream output from a pipe
	streamOutput := func(pipe io.ReadCloser, output io.Writer) {
		scanner := bufio.NewScanner(pipe)
		for scanner.Scan() {
			fmt.Fprintln(output, scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading pipe: %v\n", err)
		}
	}

	// Stream stdout and stderr concurrently
	go streamOutput(stdoutPipe, os.Stdout)
	go streamOutput(stderrPipe, os.Stderr)

	// Wait for the command to finish
	if err := cmd.Wait(); err != nil {
		fmt.Fprintf(os.Stderr, "Command finished with error: %v\n", err)
	}

	// Remove directory
	return os.RemoveAll(directory)
}

// Updated function to handle .tar.gz files
func extractTarGz(tarGzFilePath, dest string) error {
	// Open the .tar.gz file
	file, err := os.Open(tarGzFilePath)
	if err != nil {
		return err
	}
	defer file.Close()

	// Create a gzip reader to decompress the file
	gzReader, err := gzip.NewReader(file)
	if err != nil {
		return err
	}
	defer gzReader.Close()

	// Create a tar reader from the decompressed stream
	tarReader := tar.NewReader(gzReader)

	// Iterate through the tar contents
	for {
		header, err := tarReader.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}

		target := filepath.Join(dest, header.Name)
		switch header.Typeflag {
		case tar.TypeDir:
			if err := os.MkdirAll(target, os.ModePerm); err != nil {
				return err
			}
		case tar.TypeReg:
			outFile, err := os.Create(target)
			if err != nil {
				return err
			}
			defer outFile.Close() // Ensure the file is closed after writing
			if _, err := io.Copy(outFile, tarReader); err != nil {
				return err
			}
		default:
			return fmt.Errorf("unsupported type: %c in %s", header.Typeflag, header.Name)
		}
	}
	return nil
}

func isRoot() bool {
	return os.Geteuid() == 0
}

func main() {
	if !isRoot() {
		fmt.Println("This program requires root privileges.")
		os.Exit(1)
	}

	installer := &GenericInstaller{}
	if len(os.Args) < 2 {
		fmt.Println("No file provided. Pass file path as first argument.")
		os.Exit(1)
	}
	file := os.Args[1]
	if err := installer.Install(file); err != nil {
		log.Fatal(err)
	}
}




