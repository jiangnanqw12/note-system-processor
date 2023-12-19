## markdown_processor


## 需求1
格式化 字幕,代码等,方便输入chatgpt. 生成相关总结内容.

## 需求2--视频分段笔记
然后根据总结的时间戳生成拆分的视频笔记


## Book Workflow
- Download books from zlib.
- Categorize books using the CLC classification system based on their ISBN or filename.
- Determine the book's filename, preferably in English.
- Create a root directory for book notes based on the book's filename.
- Initialize the note folder structure.
- Store PDF files under the 'big assets' subfolder within the 'assets' folder.
- Add bookmarks to the PDF.
- Annotate the PDF to emphasize key points.
- Convert the PDF into plain text.
- Transform the plain text into markdown.
- Add headings to the markdown.
- Use ChatGPT to check spelling and grammar in the markdown.
- Write summaries for each chapter following the heading structure.
- Complete the markdown with images, tables, footnotes, endnotes, etc.
- Integrate the key points into your personal knowledge system.

```mermaid
graph TD
    Node_1["Download Books from zlib"]
    Node_2["Categorize Books Using CLC System Based on ISBN or Filename"]
    Node_3["Determine Book's Filename (Preferably in English)"]
    Node_4["Create Root Directory for Book Notes Based on Filename"]
    Node_4_1["Initialize Note Folder Structure"]
    Node_5["Store PDFs in 'big assets' Subfolder Under 'assets'"]
    Node_6["Add Bookmarks to PDF"]
    Node_7["Annotate PDF for Key Points"]
    Node_8["Convert PDF to Plain Text"]
    Node_9["Transform Plain Text into Markdown"]
    Node_10["Add Headings to Markdown"]
    Node_11["Use ChatGPT for Spelling and Grammar Check in Markdown"]
    Node_12["Write Chapter Summaries Based on Headings"]
    Node_13["Complete Markdown with Images, Tables, Footnotes, Endnotes"]


    Node_1 --> Node_2
    Node_2 --> Node_3
    Node_3 --> Node_4
    Node_4-->Node_4_1
    Node_4_1 --> Node_5
    Node_5 --> Node_6
    Node_6 --> Node_7
    Node_5 --> Node_8
    Node_8 --> Node_9
    Node_9 --> Node_10
    Node_10 --> Node_11
    Node_7 --> Node_12
    Node_11 --> Node_12
    Node_12 --> Node_13
    Node_12 --> output
subgraph output ["Output"]
  Node_6_1702953694["Note Taking (Visual Methods)"] --> Node_7_1702953694[Active Recall]
  Node_7_1702953694 --> Node_8_1702953694[Sleep and Physical Exercise]
  Node_8_1702953694 --> Node_9_1702953694[Feedback and Reflection]
  Node_9_1702953694 --> Node_10_1702953694["Integrate Knowledge into Personal Framework"]
end

```

## mermaid Workflow

- Change Node_\d{1,3}_timestamp1 to Node__\d{1,3}_timestamp1.
  - This step to prevent the modification of already standardized node names:
- Change Node\d{1,3} to Node_\d{1,3}.
- Change Node_\d{1,3} to Node_\d{1,3}_timestamp2.
- Change Node__\d{1,3}_timestamp1 to Node_\d{1,3}_timestamp1.

```mermaid
graph TD
    subgraph sub_1["Prevention"]
    Node_1["Node_\d{1,3}_timestamp1"]-->Node_1_1["Node__\d{1,3}_timestamp1"]
    Node_2["Node__\d{1,3}_timestamp1"]-->Node_2_2["Node_\d{1,3}_timestamp1"]
    end
    subgraph sub_2["Convertion"]
    Node_1_1-->Node_3["Node\d{1,3}"]-->Node_4["Node_\d{1,3}"]
    Node_4-->Node_5["Node_\d{1,3}_timestamp2"]-->Node_2
    end

```