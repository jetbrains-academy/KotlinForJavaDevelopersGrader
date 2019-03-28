package strings

import org.junit.Assert
import org.junit.Test
import strings.getPattern

class Tests {

    @Test
    fun match() {
        Assert.assertTrue("The pattern should match ${"10 APR 1952"}", "10 APR 1952".matches(getPattern().toRegex()))
    }
}