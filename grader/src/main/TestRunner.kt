
import com.google.gson.GsonBuilder
import com.google.gson.annotations.Expose
import org.junit.Test
import org.junit.runner.Description
import org.junit.runner.JUnitCore
import org.junit.runner.Result
import org.junit.runner.notification.RunListener
import org.junit.runners.model.TestClass
import java.io.*


object TestRunner {
  private fun getFeedback(feedback: Feedback): String =
    GsonBuilder().excludeFieldsWithoutExposeAnnotation().create().toJson(feedback)


  @JvmStatic
  @Throws(ClassNotFoundException::class)
  fun main(args: Array<String>) {
    val testClasses = mutableListOf<Class<*>>()
    val listFiles = File("build/${args[0]}").listFiles()
    for (testClass in listFiles) {
      if (!testClass.name.endsWith(".class")) {
        continue
      }
      val qualifiedName = "${args[0].replace("/", ".")}.${testClass.nameWithoutExtension}"
      val clazz = TestRunner::class.java.classLoader.loadClass(qualifiedName)
      if (TestClass(clazz).getAnnotatedMethods(Test::class.java).isNotEmpty()) {
        testClasses.add(clazz)
      }
    }
    val runner = JUnitCore()
    runner.addListener(object : RunListener() {
      val systemOut = System.out
      val fileOut = File("output.txt")

      override fun testRunStarted(description: Description?) {
        System.setOut(PrintStream(FileOutputStream(fileOut)))
        super.testRunStarted(description)
      }

      override fun testRunFinished(result: Result) {
        System.setOut(systemOut)
        fileOut.delete()
        if (result.wasSuccessful()) {
          println(getFeedback(Feedback(true, 1.0)))
        }
        else {
          val firstFailure = result.failures[0]
          val exception = firstFailure.exception

          val message: String = if (exception != null && exception !is AssertionError) {
            val sw = StringWriter()
            exception.printStackTrace(PrintWriter(sw))
            "Exception occurred:\n$sw"
          } else {
            firstFailure.message
          }
          println(getFeedback(Feedback(false, 0.0, message)))
        }
      }
    })
    runner.run(*testClasses.toTypedArray())
  }

  class Feedback(val isSuccessful: Boolean, @field:Expose val fractionalScore: Double,
                 @field:Expose val feedback: String = "Congrats! All test cases passed!")
}