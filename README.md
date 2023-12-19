## markdown_processor


## 需求1
格式化 字幕,代码等,方便输入chatgpt. 生成相关总结内容.

## 需求2--视频分段笔记
然后根据总结的时间戳生成拆分的视频笔记


## book 工作流
从 zlib下载书籍
根据书籍ISBN或者文件名,纳入CLC分类系统
确定书籍文件名,最好用英文名
根据书籍的文件名,创建书籍笔记的根目录
并初始化笔记文件夹结构
pdf文件放到assets文件夹的下的big assets文件夹下
对pdf进行添加书签,对内容分段
annotate pdf 进行内容key points 标注
将pdf转成plain text
将plain text 转成 markdown
为markdown添加head标题
并用chatgpt校对单词拼写和语法
根据head结构编写每个章节的总结
为markdown补全图片及表格,脚注,endnotes等
将key points 纳入到自己的知识体系中

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