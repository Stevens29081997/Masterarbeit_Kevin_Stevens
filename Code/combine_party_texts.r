
# Set working directory
base_dir <- "Placeholder for working directory"

# Folders to exclude:
exclude_folders <- c("Corpus_lemmatized", "raw_programme")

# Get all top-level party folders except excluded ones
party_folders <- list.dirs(base_dir, full.names = TRUE, recursive = FALSE)
party_folders <- party_folders[!basename(party_folders) %in% exclude_folders]

# Iterate over each party folder
for (party_folder in party_folders) {
  party_name <- basename(party_folder)

  # Define subfolders to include
  include_subfolders <- c("Parteiprogramm", "Reden")

  # Collect all .txt files from these subfolders, excluding "Lemmatisiert"
  txt_files <- c()
  for (subfolder in include_subfolders) {
    subfolder_path <- file.path(party_folder, subfolder)
    if (dir.exists(subfolder_path)) {
      # List all .txt files in this subfolder and its subdirectories, excluding any path containing "Lemmatisiert"
      files <- list.files(subfolder_path, pattern = "\\.txt$", recursive = TRUE, full.names = TRUE)
      files <- files[!grepl("Lemmatisiert", files)]
      txt_files <- c(txt_files, files)
    }
  }

  # Combine contents if there are files
  if (length(txt_files) > 0) {
    combined_text <- c()
    for (file in txt_files) {
      lines <- readLines(file, encoding = "UTF-8", warn = FALSE)
      combined_text <- c(combined_text, lines)
    }

    # Output file path
    output_file <- file.path(party_folder, paste0(party_name, "_combined.txt"))

    # Write combined text to file
    writeLines(combined_text, output_file, useBytes = TRUE)
    cat("Combined file created for party:", party_name, "at", output_file, "
")
  } else {
    cat("No files found for party:", party_name, "
")
  }
}

