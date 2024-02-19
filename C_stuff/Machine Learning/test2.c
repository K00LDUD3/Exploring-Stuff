#include <stdio.h>
#include <stdlib.h>

struct tree
{
    int dim;
    struct tree **children;
    int childrenLength;
    double value;
};

void display(struct tree *root)
{
    if (root->children == NULL)
    {
        printf("%.2lf\n", root->value);
        return;
    }

    for (int i = 0; i < root->childrenLength; i++)
    {
        display(*(root->children + i));
    }
}

void create(struct tree *root, int *dims, int num_dims)
{
    if (num_dims == 0)
    {
        root->children = NULL;
        root->childrenLength = 0;
        root->dim = 0;
        scanf("%lf", &root->value);
        return;
    }

    int *new_dims = malloc((num_dims - 1) * sizeof(int));
    for (int i = 1; i < num_dims; i++)
    {
        *(new_dims + i - 1) = *(dims + i);
    }

    struct tree **children = malloc(*dims * sizeof(struct tree *));
    for (int i = 0; i < *dims; i++)
    {
        *(children + i) = malloc(sizeof(struct tree *));
        children[i]->dim = num_dims - 1;
        children[i]->childrenLength = *dims;
        create(*(children + i), new_dims, num_dims - 1);
    }
}

int main()
{
    struct tree *root = malloc(sizeof(struct tree *));
    root->childrenLength = 2;
    int dims[1] = {2};
    create(root, dims, 1);
    display(root);
}