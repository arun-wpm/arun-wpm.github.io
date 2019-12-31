#include <stdio.h>
int main()
{
    int bit, top = 1 << 30;
    int test, maxbits = 0, max, cnt, d;
    for (bit = 0; bit < top; bit++)
    {
        for (d = 1; d <= 14; d++)
            if (bit & (bit >> d) & (bit >> 2*d))
                break;
        if (d == 15)
        {
            cnt = 0;
            for (d = 0; d < 30; d++)
                if (bit&(1 << d))
                    cnt++;
            // printf("%d %d\n", bit, cnt);
            if (cnt > maxbits)
            {
                maxbits = cnt;
                max = bit;
                printf("%d %d\n", bit, cnt);
            }
        }
    }
    printf("%d %d\n", max, maxbits);
    for (d = 0; d < 30; d++)
        if (max&(1 << d))
            printf("1");
        else
            printf("0");
}
