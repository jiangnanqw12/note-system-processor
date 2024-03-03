# Regular Expression Utilities

pattern_code_block = r"^    ```(\n[\s\S]*?\n)    ```$"
replacement_code_block = r"    ```python$1    ```"
pattern_star_bullet_list_to_dash_list = r"^(\s*)\*"
replacement_star_bullet_list_to_dash_list = r"\1- "

pattern_old_sub = r'\[\[\d{1,2}:(\d{1,2}:\d{1,2}),\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3}\],\[(.*)\]\]'
"""
[[00:00:00,330 --> 00:00:01,750],[哈喽，大家好，我是王刚。]]
"""
replacement_old_sub = r'(\1) \2'
replacement_old_sub2 = r'($1) $2'

pattern_zotero_annotation_with_citation = r'“(.+?)” \((\[.+?\]\(zotero://select/.+\))\) \(\[(.+?)\]\((zotero://open-pdf/.+?)\)\)[ ]*(.*)'
"""
“CHAPTER 2 EASY DOES IT” ([Oakley et al., 2018, p. 28](zotero://select/library/items/64PPK6GW)) ([pdf](zotero://open-pdf/library/items/LZC7SR86?page=28&annotation=H5EPTVN8)) Why Trying Too Hard Can Sometimes Be Part of the Problem

"""
replacement_zotero_annotation_with_citation_2_mindmap = r'\1 [📖](\4 "\5")'
replacement_zotero_annotation_with_citation_2_mindmap_2 = r'$1 [📖]($4 "$5")'

pattern_mindmap_smart_quotation_marks_and_pdf_text = r'(^\s*-) “(.+?)” \(\[(pdf)\]\((zotero://open-pdf/.+?)\)\)'
replacement_mindmap_smart_quotation_marks_and_pdf_text = r'$1 $2 [📖]($4)'

pattern_mmb_hightlight_citation_comment = r'(^\s*-) “(.+?)” \((\[.+?\]\(zotero://select/.+\))\) \(\[(.+?)\]\((zotero://open-pdf/.+?)\)\)[ ]*(.*)'
"""
        - “taking action” ([Forte, 2023, p. 6](zotero://select/library/items/ZLT3U9AA)) ([pdf](zotero://open-pdf/library/items/J46CETWT?page=6&annotation=KTHHS3TM))
"""
replacement_mmb_hightlight_citation_comment = r'$1 $2 [📖]($5 "$6")'
replacement_mmb_hightlight_citation_comment2 = r'\1 \2 [📖](\5 "\6")'
pattern_md_hightlight_citation_comment = r'^“(.+?)” \((\[.+?\]\(zotero://select/.+\))\) \(\[(.+?)\]\((zotero://open-pdf/.+?)\)\)[ ]*(.*)'
"""
“taking action” ([Forte, 2023, p. 6](zotero://select/library/items/ZLT3U9AA)) ([pdf](zotero://open-pdf/library/items/J46CETWT?page=6&annotation=KTHHS3TM))
"""
replacement_md_hightlight_citation_comment = r'$1 [📖]($4 "$5")'
replacement_md_hightlight_citation_comment2 = r'\1 [📖](\4 "\5")'
pattern_mmb_clc_index_node_old_to_new = r"^(\s*-) ([A-Z].*?)_(.+)"
replacement_mmb_clc_index_node_old_to_new = r"$1 $2 [📄]($2)"

pattern_mmb_bullet_list_wiki_link = r"^(\s*-)\s+\[\[(.+)\]\]"
replacement_mmb_bullet_list_wiki_link = r"$1 $2 [📄]($2)"


pattern_subtile_summary_gpt_timestamps_files = r"(subtitle|summary_gpt|timestamps)_(\d{10})\.md"
"""
subtitle_1698658249.md
"""
replacement_subtile_summary_gpt_timestamps_files1 = r"\1_\2.text"
replacement_subtile_summary_gpt_timestamps_files2 = r"$1_$2.text"
