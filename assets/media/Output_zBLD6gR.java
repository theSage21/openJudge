import java.util.Scanner;

public class Output {
    public static void main(String[] args) {
        int[] numbers;
        Scanner in = new Scanner(System.in);
        int numberOfNumbers = in.nextInt();
        int number;
        for (int i = 0; i < numberOfNumbers; i++) {
            int pos = i + 1;
            number = in.nextInt(); 
            System.out.println("" + (number * number));   
        }
    }
}
