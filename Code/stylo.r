
# Load package
library(stylo)

# Set working directory. For non-lemmatized texts, change folder here to "...Corpus_combined".
setwd("C:/Users/Data/Corpus_lemmatized")

# Start Stylo analysis
stylo(
  gui = FALSE,                # Deactivate GUI, as we determine everything via code
  corpus.dir = ".",           # Current directory with the TXT files
  analysis.type = "PCV",      # Cluster Analysis for similarity comparison (=“CA”) / or Principal Component Visualization (=“PCV”)
  mfw.min = 100,              # Minimum frequent words ( adjustable)
  mfw.max = 500,              # Maximum frequent words ( adjustable)
  mfw.incr = 500,             # Increment
  distance.measure = "cosine",# Similarity measure
  sampling = "no.sampling",   # No sampling, use entire texts
  write.png.file = TRUE       # Save result as PNG
)

