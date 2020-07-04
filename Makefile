
prepare:
	- npm install hexo-cli
	- git clone --depth=1 https://github.com/wuchong/jacman.git themes/jacman
	- cp config/jacman_config.yml themes/jacman/_config.yml

generate:
	hexo g

clean:
	hexo clean

deploy: prepare generate
