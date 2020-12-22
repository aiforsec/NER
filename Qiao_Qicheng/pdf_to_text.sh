# shellcheck disable=SC2043
# to convert all files in ./raw_pdf to text and store in ./raw_txt
for fn in ./raw_pdf/*.pdf ; do
  pdftotext "$fn" "./raw_text/$(basename $fn).txt"
#  echo $fn
done