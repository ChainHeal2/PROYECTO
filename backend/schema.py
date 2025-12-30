esquema = [
    'SET FOREIGN_KEY_CHECKS = 0;',
    'DROP TABLE IF EXISTS usuario;',
    'SET FOREIGN_KEY_CHECKS = 1;',"""
          
CREATE TABLE `usuario` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `usuario_UNIQUE` (`usuario`)
)
"""]