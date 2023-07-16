import re


def split_text(text, max_length=100):
    # 句読点、読点、改行で分割する
    segments = re.split(r"([。\n])", text)
    result = []
    current_segment = ""
    for segment in segments:
        # 現在のセグメントに追加しても最大長を超えない場合
        if len(current_segment) + len(segment) <= max_length:
            current_segment += segment
        else:
            # 現在のセグメントを結果に追加
            result.append(current_segment)
            current_segment = segment
    # 最後のセグメントを結果に追加
    if current_segment:
        result.append(current_segment)
    return result
