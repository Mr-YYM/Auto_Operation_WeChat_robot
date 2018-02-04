import wxpy
import data_getter

contents = data_getter.read_contents_from_readhub()
str_cts = []
for k, v in contents.items():
    str_cts.append('【%s】\n%s\n' % (k, v))
show_cts = '------------------\n'.join(str_cts)

# bot = wxpy.Bot()

print(show_cts)
