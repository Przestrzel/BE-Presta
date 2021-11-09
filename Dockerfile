FROM prestashop/prestashop:1.7.7.8

RUN a2enmod rewrite

RUN chmod a+rwx -R project-dir/smarty.cache.dir