# spring 常用注解笔记

- `@ConditionalOnBean`
如果`ConditionalOnBean`中标注的类或者bean被注入了，则会将注解标记的bean注入到spring中，如果未注入则标记的bean不被注入
``` java
@ConditionalOnBean(EurekaServerMarkerConfiguration.Marker.class)
public class EurekaServerAutoConfiguration implements WebMvcConfigurer {
```

- `@Import`