import java.nio.file.{Files, Paths, StandardOpenOption}
import java.nio.charset.StandardCharsets

@main def exec(cpgFile: String, targetStr: String, outFile: String) = {
   importCpg(cpgFile)

   // 将传入的字符串转换为目标列表
   val targets = targetStr.split(",").toList.distinct

   // 创建或清空输出文件
   Files.write(Paths.get(outFile), "".getBytes(StandardCharsets.UTF_8))

   // 遍历 targets 列表，将结果合并到同一个文件中
   targets.foreach { target =>
      try {
         // 获取当前 target 的结果
         val result = cpg.method(cpg.call(target).method.name.l(0)).dotPdg.l.mkString("\n")

         // 如果结果为空，则跳过该 target
         if (result.nonEmpty) {
            val output = s"Results for target: $target\n$result\n\n"
            
            // 追加结果到输出文件
            Files.write(Paths.get(outFile), output.getBytes(StandardCharsets.UTF_8), StandardOpenOption.APPEND)
            println(s"Output written for target: $target")
         } else {
            println(s"No result found for target: $target, skipping.")
         }
      } catch {
         case e: Exception =>
            // 捕获异常并输出错误信息，跳过当前 target
            println(s"Error processing target: $target, skipping. Error: ${e.getMessage}")
      }
   }
}
