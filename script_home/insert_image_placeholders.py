import os
import re
from datetime import datetime

def insert_images(content_dir):
    log_messages = [f"--- 圖片標籤插入: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---"]
    updated_count = 0

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 更聰明的檢查：如果發現任何格式的 <imageX> 就跳過
                if re.search(r'<image\d*>', content):
                    continue

                lines = content.split('\n')
                new_lines = []
                img_count = 1
                in_front_matter = 0
                has_h2 = False

                for line in lines:
                    if line.strip() == "---":
                        in_front_matter += 1
                    
                    # 只有在 Front Matter 結束後才處理 ## 標題
                    if in_front_matter >= 2 and line.startswith("## "):
                        new_lines.append(f"<image{img_count}></image{img_count}>\n")
                        img_count += 1
                        has_h2 = True
                    
                    new_lines.append(line)

                if has_h2:
                    content = '\n'.join(new_lines)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    log_messages.append(f"[插入圖片] {file}: 插入了 {img_count-1} 個標籤")
                    updated_count += 1

    if updated_count == 0:
        log_messages.append("未發現需要插入標籤的檔案。")

    # 寫入日誌
    output_path = os.path.join(os.path.dirname(__file__), "output.txt")
    with open(output_path, 'a', encoding='utf-8') as log_file:
        log_file.write("\n".join(log_messages) + "\n\n")
    print(f"圖片標籤處理完成，更新了 {updated_count} 個檔案。日誌：{output_path}")

if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(__file__), "../content")
    insert_images(target_dir if os.path.exists(target_dir) else "content")