# Define your site below.
# Run the compiler and it will generate HTML, create a GitHub repo, and deploy to Vercel.

site "my-portfolio" {
  title       = "Iris Ayala — UVG 2026"
  description = "CS student building compilers at Universidad del Valle de Guatemala"
  theme       = "dark"

  page "index" {
    hero    = "Hello, I am Iris Ayala and I built this site with a compiler I wrote!"
    about   = "I am a CS student at UVG. This page was generated from a custom DSL, pushed to GitHub, and deployed to Vercel — all by my ANTLR compiler."
    contact = "aya23965@uvg.edu.gt"
  }
}
