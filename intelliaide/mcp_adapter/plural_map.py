"""GVK resolution helper for must-gather directory names.

Maps plural directory names (as found in must-gather archives) to their
singular Kind and apiVersion strings needed by MCP tool calls.
"""

# Mapping: plural directory name -> (Kind, apiVersion)
# Covers the ~50 most common resources IntelliAide typically selects.
PLURAL_TO_KIND = {
    # Core (api_group = "core" or empty in must-gather dirs)
    "pods": ("Pod", "v1"),
    "services": ("Service", "v1"),
    "endpoints": ("Endpoints", "v1"),
    "configmaps": ("ConfigMap", "v1"),
    "secrets": ("Secret", "v1"),
    "serviceaccounts": ("ServiceAccount", "v1"),
    "persistentvolumeclaims": ("PersistentVolumeClaim", "v1"),
    "persistentvolumes": ("PersistentVolume", "v1"),
    "nodes": ("Node", "v1"),
    "namespaces": ("Namespace", "v1"),
    "events": ("Event", "v1"),
    "replicationcontrollers": ("ReplicationController", "v1"),
    "resourcequotas": ("ResourceQuota", "v1"),
    "limitranges": ("LimitRange", "v1"),

    # apps
    "deployments": ("Deployment", "apps/v1"),
    "daemonsets": ("DaemonSet", "apps/v1"),
    "statefulsets": ("StatefulSet", "apps/v1"),
    "replicasets": ("ReplicaSet", "apps/v1"),
    "controllerrevisions": ("ControllerRevision", "apps/v1"),

    # batch
    "jobs": ("Job", "batch/v1"),
    "cronjobs": ("CronJob", "batch/v1"),

    # networking
    "ingresses": ("Ingress", "networking.k8s.io/v1"),
    "networkpolicies": ("NetworkPolicy", "networking.k8s.io/v1"),

    # rbac
    "clusterroles": ("ClusterRole", "rbac.authorization.k8s.io/v1"),
    "clusterrolebindings": ("ClusterRoleBinding", "rbac.authorization.k8s.io/v1"),
    "roles": ("Role", "rbac.authorization.k8s.io/v1"),
    "rolebindings": ("RoleBinding", "rbac.authorization.k8s.io/v1"),

    # storage
    "storageclasses": ("StorageClass", "storage.k8s.io/v1"),
    "volumeattachments": ("VolumeAttachment", "storage.k8s.io/v1"),
    "csidrivers": ("CSIDriver", "storage.k8s.io/v1"),
    "csinodes": ("CSINode", "storage.k8s.io/v1"),

    # policy
    "poddisruptionbudgets": ("PodDisruptionBudget", "policy/v1"),

    # autoscaling
    "horizontalpodautoscalers": ("HorizontalPodAutoscaler", "autoscaling/v2"),

    # config.openshift.io
    "clusteroperators": ("ClusterOperator", "config.openshift.io/v1"),
    "clusterversions": ("ClusterVersion", "config.openshift.io/v1"),
    "infrastructures": ("Infrastructure", "config.openshift.io/v1"),
    "networks": ("Network", "config.openshift.io/v1"),
    "oauths": ("OAuth", "config.openshift.io/v1"),
    "ingresses.config.openshift.io": ("Ingress", "config.openshift.io/v1"),
    "proxies": ("Proxy", "config.openshift.io/v1"),
    "schedulers": ("Scheduler", "config.openshift.io/v1"),
    "apiservers": ("APIServer", "config.openshift.io/v1"),
    "featuregates": ("FeatureGate", "config.openshift.io/v1"),
    "operatorhubs": ("OperatorHub", "config.openshift.io/v1"),
    "images.config.openshift.io": ("Image", "config.openshift.io/v1"),
    "dnses": ("DNS", "config.openshift.io/v1"),

    # operator.openshift.io
    "etcds": ("Etcd", "operator.openshift.io/v1"),
    "kubeapiservers": ("KubeAPIServer", "operator.openshift.io/v1"),
    "kubecontrollermanagers": ("KubeControllerManager", "operator.openshift.io/v1"),
    "openshiftapiservers": ("OpenShiftAPIServer", "operator.openshift.io/v1"),
    "authentications.operator.openshift.io": ("Authentication", "operator.openshift.io/v1"),
    "consoles.operator.openshift.io": ("Console", "operator.openshift.io/v1"),
    "ingresscontrollers": ("IngressController", "operator.openshift.io/v1"),

    # machine.openshift.io
    "machines": ("Machine", "machine.openshift.io/v1beta1"),
    "machinesets": ("MachineSet", "machine.openshift.io/v1beta1"),
    "machinehealthchecks": ("MachineHealthCheck", "machine.openshift.io/v1beta1"),

    # machineconfiguration.openshift.io
    "machineconfigs": ("MachineConfig", "machineconfiguration.openshift.io/v1"),
    "machineconfigpools": ("MachineConfigPool", "machineconfiguration.openshift.io/v1"),

    # monitoring
    "prometheusrules": ("PrometheusRule", "monitoring.coreos.com/v1"),
    "servicemonitors": ("ServiceMonitor", "monitoring.coreos.com/v1"),
    "alertmanagers": ("Alertmanager", "monitoring.coreos.com/v1"),

    # certificates
    "certificates": ("Certificate", "cert-manager.io/v1"),
    "certificatesigningrequests": ("CertificateSigningRequest", "certificates.k8s.io/v1"),

    # apiextensions
    "customresourcedefinitions": ("CustomResourceDefinition", "apiextensions.k8s.io/v1"),
}

# Maps the api_group directory name in must-gather to the full apiVersion string.
# Must-gather stores resources under: cluster-scoped-resources/<api_group>/<resource>.yaml
API_GROUP_TO_VERSION = {
    "core": "v1",
    "": "v1",
    "apps": "apps/v1",
    "batch": "batch/v1",
    "networking.k8s.io": "networking.k8s.io/v1",
    "rbac.authorization.k8s.io": "rbac.authorization.k8s.io/v1",
    "storage.k8s.io": "storage.k8s.io/v1",
    "policy": "policy/v1",
    "autoscaling": "autoscaling/v2",
    "apiextensions.k8s.io": "apiextensions.k8s.io/v1",
    "admissionregistration.k8s.io": "admissionregistration.k8s.io/v1",
    "certificates.k8s.io": "certificates.k8s.io/v1",
    "coordination.k8s.io": "coordination.k8s.io/v1",
    "scheduling.k8s.io": "scheduling.k8s.io/v1",
    "config.openshift.io": "config.openshift.io/v1",
    "operator.openshift.io": "operator.openshift.io/v1",
    "machine.openshift.io": "machine.openshift.io/v1beta1",
    "machineconfiguration.openshift.io": "machineconfiguration.openshift.io/v1",
    "monitoring.coreos.com": "monitoring.coreos.com/v1",
    "route.openshift.io": "route.openshift.io/v1",
    "image.openshift.io": "image.openshift.io/v1",
    "build.openshift.io": "build.openshift.io/v1",
    "apps.openshift.io": "apps.openshift.io/v1",
    "oauth.openshift.io": "oauth.openshift.io/v1",
    "user.openshift.io": "user.openshift.io/v1",
    "security.openshift.io": "security.openshift.io/v1",
    "quota.openshift.io": "quota.openshift.io/v1",
    "template.openshift.io": "template.openshift.io/v1",
    "cert-manager.io": "cert-manager.io/v1",
    "snapshot.storage.k8s.io": "snapshot.storage.k8s.io/v1",
}


def resolve_kind(plural_name: str) -> tuple:
    """Resolve a plural directory name to (Kind, apiVersion).

    Returns (Kind, apiVersion) if known, otherwise (plural_name, "") as fallback.
    """
    entry = PLURAL_TO_KIND.get(plural_name.lower())
    if entry:
        return entry
    return (plural_name, "")


def resolve_api_version(api_group: str) -> str:
    """Resolve an API group directory name to its full apiVersion string.

    Returns the apiVersion if known, otherwise returns the group name with /v1 appended.
    """
    if not api_group:
        return "v1"
    version = API_GROUP_TO_VERSION.get(api_group)
    if version:
        return version
    # Fallback: assume v1 for the group
    return f"{api_group}/v1"
