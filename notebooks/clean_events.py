from tqdm import tqdm


def clean_line_with_too_many_tabs(bad_line):
    l = len(bad_line)
    i = 0
    to_delete = [-1]
    while -1 < i < l:
        i = bad_line.find('"', i+1)
        if i < 0:
            break
        next_quote = bad_line.find('"', i+1)
        next_tab = bad_line.find('\t', i+1)
        while -1 < next_tab < next_quote:
            to_delete.append(next_tab)
            next_tab = bad_line.find('\t', next_tab+1)
        i = next_quote

    to_delete.append(l)
    new_string = "".join([bad_line[a+1:to_delete[i+1]] for i, a in enumerate(to_delete[:-1])])
    return new_string


if __name__ == '__main__':
    clean_lines = []
    right_n_tabs = 113
    save_freq = 1000000
    total_lines = 71180735
    with open('Z:\\event.tsv', 'r', encoding='utf-8') as f:
        for i in tqdm(range(total_lines)):
            l = f.readline()
            if not l:
                break
            n_tabs = l.count('\t')
            if n_tabs != right_n_tabs:
                while n_tabs < right_n_tabs:
                    ll = f.readline()
                    l = l[:-1] + ll
                    n_tabs = l.count('\t')
                if n_tabs > right_n_tabs:
                    l = clean_line_with_too_many_tabs(l)
                    n_tabs = l.count('\t')
            if n_tabs != right_n_tabs:
                print(f'Could not fix line {i}:\n{l}')

            clean_lines.append(l)
            
            if (i+1) % save_freq == 0:
                with open('Z:\\event_fixed.tsv', 'a', encoding='utf-8') as f_write:
                    f_write.write(''.join(clean_lines))
                clean_lines = []
                      
    with open('Z:\\event_fixed.tsv', 'a', encoding='utf-8') as f_write:
        f_write.write(''.join(clean_lines))
        
