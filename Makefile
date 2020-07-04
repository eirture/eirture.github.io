
prepare:
	- npm install hexo-cli
	- git clone --depth=1 https://github.com/wuchong/jacman.git theme/jacman
	- cp config/jacman_config.yml theme/jacman/_config.yml

generate:
	hexo g

clean:
	hexo clean
