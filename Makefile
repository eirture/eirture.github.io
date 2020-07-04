
prepare:
	- npm install 
	- git clone --depth=1 https://github.com/wuchong/jacman.git themes/jacman
	- cp -r custom/* themes/

generate:
	./node_modules/hexo/bin/hexo g

clean:
	./node_modules/hexo/bin/hexo clean

deploy: prepare generate
