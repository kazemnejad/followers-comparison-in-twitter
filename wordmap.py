from os import path

from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words


def create_word_map(username):
    # additional_stopwords = open("stop_words_%s.txt" % username, encoding="utf8").read().split()

    text = open("words_%s.txt" % username, encoding='utf-8').read()

    wordcloud = PersianWordCloud(
        max_words=100,
        margin=0,
        width=800,
        height=800,
        min_font_size=1,
        max_font_size=500,
        background_color="black"
    ).generate(text)

    image = wordcloud.to_image()
    image.show()
    image.save()


def create_freq_file(username):
    words = {}
    with open("words_%s.txt" % username, encoding='utf-8') as f:
        count = 0
        for line in f:
            for w in line.split():
                words[w] = words.get(w, 0) + 1
                count += 1

    for key in words:
        words[key] = words[key] * 1.0 / count

    freqs = [p for p in words.items()]
    freqs.sort(key=lambda x: x[1], reverse=True)

    with open("word_freqs_%s.txt" % username, "w", encoding="utf8") as f:
        for freq in freqs:
            f.write("%s\t%s" % (freq[0], freq[1]))
            f.write("\n")


def create_dif_common_freq_file(username1, username2):
    freq1, freq2 = {}, {}

    count = 0
    with open("word_freqs_%s.txt" % username1, "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            word, freq = line.split()
            freq1[word] = float(100 - count)
            count += 1

            if count > 100:
                break

    count = 0
    with open("word_freqs_%s.txt" % username2, "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            word, freq = line.split()
            freq2[word] = float(100 - count)
            count += 1

            if count > 100:
                break

    words1 = set(freq1.keys())
    words2 = set(freq2.keys())

    diff_freq = {}
    for w in words1:
        if w in words2:
            freq = abs(freq1[w] - freq2[w])
            diff_freq[w] = freq

    common_freq = {}
    max_diff = max(diff_freq.values())
    for (w, f) in diff_freq.items():
        common_freq[w] = abs(max_diff - f)

    with open("word_dif_freq_%s_%s.txt" % (username1, username2), "w", encoding="utf8") as file:
        diff_freq = list(diff_freq.items())
        diff_freq.sort(key=lambda x: x[1], reverse=True)
        diff_freq = diff_freq[:50]
        for (w, f) in diff_freq:
            file.write("%s: %s" % (int(f), w))
            file.write("\n")

    with open("sword_common_freq_%s_%s.txt" % (username1, username2), "w", encoding="utf8") as file:
        common_freq = list(common_freq.items())
        common_freq.sort(key=lambda x: x[1], reverse=True)
        common_freq = common_freq[:50]
        for (w, f) in common_freq:
            file.write("%s: %s" % (int(f), w))
            # file.write("\n".join([w] * int(f)))
            # file.write("%s: %s" % (int(f), w))
            file.write("\n")


def create_dif_freq_file_single(username1, username2):
    freq1, freq2 = {}, {}

    count = 0
    with open("word_freqs_%s.txt" % username1, "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            word, freq = line.split()
            freq1[word] = float(100 - count)
            count += 1

            if count > 100:
                break

    count = 0
    with open("word_freqs_%s.txt" % username2, "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            word, freq = line.split()
            freq2[word] = float(100 - count)
            count += 1

            if count > 100:
                break

    diff_freq = {}
    for w in freq1:
        freq = freq1[w] - freq2.get(w, 0)
        diff_freq[w] = freq

    with open("bias_word_dif_freq_%s_%s.txt" % (username1, username2), "w", encoding="utf8") as file:
        diff_freq = [(w, f) for (w, f) in diff_freq.items() if f > 0]
        diff_freq.sort(key=lambda x: x[1], reverse=True)
        for (w, f) in diff_freq:
            # file.write("%s: %s" % (int(f), w))
            file.write("\n".join([w] * int(f)))
            file.write("\n")
