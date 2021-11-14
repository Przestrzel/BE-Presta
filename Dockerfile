FROM prestashop/prestashop:1.7.7.8

RUN a2enmod ssl

EXPOSE 80
EXPOSE 443

RUN service apache2 restart