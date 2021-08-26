
.PHONY: prepare
prepare:
	- npm install 
	- git clone --depth=1 https://github.com/theme-next/hexo-theme-next themes/next
	- cp -r custom/* themes/

.PHONY: generate
generate:
	./node_modules/hexo/bin/hexo g

.PHONY: clean
clean:
	./node_modules/hexo/bin/hexo clean

.PHONY: deploy
deploy: prepare generate

.PHONY: service
service: 
	- cp -r custom/* themes/
	./node_modules/hexo/bin/hexo g && ./node_modules/hexo/bin/hexo s

