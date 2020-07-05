
prepare:
	- npm install 
	- git clone --depth=1 https://github.com/theme-next/hexo-theme-next themes/next
	- cp -r custom/* themes/

generate:
	./node_modules/hexo/bin/hexo g

clean:
	./node_modules/hexo/bin/hexo clean

service: 
	- cp -r custom/* themes/
	./node_modules/hexo/bin/hexo g && ./node_modules/hexo/bin/hexo s
